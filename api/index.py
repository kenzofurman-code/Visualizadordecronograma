from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
from PIL import Image
import io
import base64
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-cronograma")
async def upload_cronograma(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="O arquivo precisa ser um PDF.")
    
    try:
        # Ler o arquivo PDF diretamente da memória
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if len(doc) == 0:
            raise HTTPException(status_code=400, detail="O arquivo PDF está vazio.")
            
        page = doc[0]
        zoom = 300 / 72  # Alta definição (300 DPI)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        
        # Converter Pixmap do PyMuPDF diretamente em uma imagem PIL (em memória)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        largura, altura = img.size
        
        # Algoritmo de Varredura para achar o fim da lista de tarefas (X)
        x_cut = int(largura * 0.06)
        for x in range(0, int(largura * 0.20)):
            r, g, b = img.getpixel((x, int(altura * 0.2)))
            if r > 240 and g > 240 and b > 240:
                x_cut = x
                break
                
        # Algoritmo de Varredura para achar o fim da régua de datas (Y)
        y_cut = int(altura * 0.035)
        for y in range(0, int(altura * 0.10)):
            r, g, b = img.getpixel((x_cut + 50, y))
            if r > 250 and g > 250 and b > 250:
                y_cut = y
                break
        
        quadrantes = {
            "top_left": (0, 0, x_cut, y_cut),
            "timeline": (x_cut, 0, largura, y_cut),
            "sidebar": (0, y_cut, x_cut, altura),
            "gantt_core": (x_cut, y_cut, largura, altura)
        }
        
        urls = {}
        for nome, box in quadrantes.items():
            cropped = img.crop(box)
            
            # Salvar imagem em buffer na memória e codificar em Base64
            buffered = io.BytesIO()
            cropped.save(buffered, format="PNG", optimize=True)
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            urls[nome] = f"data:image/png;base64,{img_str}"
            
        doc.close()
        
        return JSONResponse(content={
            "sucesso": True,
            "dimensoes": {
                "largura_total": largura,
                "altura_total": altura,
                "x_cut": x_cut,
                "y_cut": y_cut
            },
            "urls": urls
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

# Servir os arquivos estáticos do frontend (raiz) para desenvolvimento local
# Isso só será acionado se a rota não corresponder a uma API (como "/index.html" ou "/")
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=parent_dir, html=True), name="static")
