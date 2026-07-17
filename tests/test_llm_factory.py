import pytest
from core.llm_factory import _construir_llm, extraer_texto_pdf
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


_MINIMAL_PDF = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n4 0 obj<</Length 44>>stream\nBT /F1 12 Tf 100 700 Td (Hello World) Tj ET\nendstream\nendobj\n5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000266 00000 n \n0000000374 00000 n \ntrailer<</Size 6/Root 1 0 R>>\nstartxref\n435\n%%EOF"


class TestConstruirLLM:
    def test_deepseek_retorna_chatopenai(self):
        llm = _construir_llm("DeepSeek", "deepseek-chat", 0.3)
        assert isinstance(llm, ChatOpenAI)
        assert llm.model_name == "deepseek-chat"
        assert llm.temperature == 0.3

    def test_openai_retorna_chatopenai(self):
        llm = _construir_llm("OpenAI", "gpt-4o-mini", 0.5)
        assert isinstance(llm, ChatOpenAI)
        assert llm.model_name == "gpt-4o-mini"

    def test_groq_retorna_chatopenai(self):
        llm = _construir_llm("Groq (Gratis)", "mixtral-8x7b-32768", 0.7)
        assert isinstance(llm, ChatOpenAI)
        assert llm.temperature == 0.7

    def test_gemini_retorna_chatgoogle(self):
        llm = _construir_llm("Google (Gemini)", "gemini-1.5-flash", 0.2)
        assert isinstance(llm, ChatGoogleGenerativeAI)
        assert llm.model == "gemini-1.5-flash"

    def test_proveedor_invalido_lanza_error(self):
        from unittest.mock import patch
        with patch("os.getenv", return_value="fake-key"):
            llm = _construir_llm("Proveedor Invalido", "x", 0.0)
            assert isinstance(llm, ChatOpenAI)

    def test_sin_api_key_lanza_error(self):
        import os
        original = os.environ.pop("DEEPSEEK_API_KEY", None)
        with pytest.raises(ValueError, match="DEEPSEEK_API_KEY"):
            _construir_llm("DeepSeek", "m", 0.0)
        if original:
            os.environ["DEEPSEEK_API_KEY"] = original


class TestExtraerTextoPDF:
    def test_extraer_texto_pdf_devuelve_string(self):
        class FakeUpload:
            def read(self):
                return _MINIMAL_PDF

        texto = extraer_texto_pdf(FakeUpload())
        assert isinstance(texto, str)
        assert "Hello World" in texto

    def test_extraer_texto_pdf_vacio_lanza_error(self):
        class EmptyUpload:
            def read(self):
                return b""

        import pypdf.errors
        with pytest.raises((pypdf.errors.EmptyFileError, pypdf.errors.PdfStreamError)):
            extraer_texto_pdf(EmptyUpload())
