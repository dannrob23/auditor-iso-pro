from database import (
    guardar_reporte, listar_reportes, obtener_reporte, stats_globales,
    guardar_vulnerabilidad, listar_vulnerabilidades, stats_vulnerabilidades,
    parsear_stats, crear_auditoria, obtener_auditorias, actualizar_auditoria,
    limpiar_vulnerabilidades_antiguas, desactivar_vulnerabilidad,
)


class TestReportes:
    def test_guardar_y_listar(self):
        stats = guardar_reporte(
            usuario="test_user",
            fuente="PDF",
            nombre_doc="test.pdf",
            proveedor="DeepSeek",
            modelo="deepseek-chat",
            resultado="| Control | ✅ CONFORME | OK | Mejorar |\n| Control2 | ⚠️ PARCIAL | OK | Mejorar |",
        )
        assert stats["conformes"] == 1
        assert stats["parciales"] == 1
        assert stats["no_conformes"] == 0
        assert stats["cumplimiento_pct"] == 75.0

        reportes = listar_reportes()
        assert len(reportes) == 1
        assert reportes[0]["usuario"] == "test_user"
        assert reportes[0]["fuente"] == "PDF"

    def test_obtener_reporte_por_id(self):
        guardar_reporte("u", "PDF", "doc.pdf", "p", "m", "| Control | ❌ NO CONFORME |")
        reportes = listar_reportes()
        r = obtener_reporte(reportes[0]["id"])
        assert r is not None
        assert r["proveedor"] == "p"

    def test_stats_globales(self):
        guardar_reporte("u1", "PDF", "a.pdf", "p", "m",
                        "| C1 | ✅ CONFORME |\n| C2 | ❌ NO CONFORME |")
        guardar_reporte("u2", "TEXTO", "b.txt", "p", "m",
                        "| C1 | ⚠️ PARCIAL |")
        sg = stats_globales()
        assert sg["total_reportes"] == 2
        assert sg["total_usuarios"] == 2

    def test_reporte_vacio_retorna_lista_vacia(self):
        assert listar_reportes() == []


class TestParsearStats:
    def test_sin_resultado(self):
        assert parsear_stats("") == {"conformes": 0, "parciales": 0, "no_conformes": 0, "cumplimiento_pct": 0.0}

    def test_todas_categorias(self):
        resultado = """| Control | Estado | Obs |
| --- | --- | --- |
| Control1 | ✅ CONFORME | OK |
| Control2 | ⚠️ PARCIAL | OK |
| Control3 | ❌ NO CONFORME | KO |"""
        stats = parsear_stats(resultado)
        assert stats["conformes"] == 1
        assert stats["parciales"] == 1
        assert stats["no_conformes"] == 1
        assert stats["cumplimiento_pct"] == 50.0

    def test_solo_conformes(self):
        resultado = "| C1 | ✅ CONFORME |\n| C2 | CONFORME |"
        stats = parsear_stats(resultado)
        assert stats["conformes"] == 2
        assert stats["cumplimiento_pct"] == 100.0

    def test_ignora_encabezados(self):
        resultado = """| Control ISO 27001 | Estado |
| --- | --- |
| C1 | ✅ CONFORME |"""
        stats = parsear_stats(resultado)
        assert stats["conformes"] == 1

    def test_porcentaje_sin_controles(self):
        assert parsear_stats("Sin datos")["cumplimiento_pct"] == 0.0


class TestVulnerabilidades:
    def test_guardar_y_listar(self):
        ok = guardar_vulnerabilidad({
            "id_vulnerabilidad": "VULN-001",
            "fuente_origen": "MITRE",
            "resumen_es": "Test vulnerability",
            "probabilidad_base": 4,
            "severidad_tecnica": 5,
        })
        assert ok

        lista = listar_vulnerabilidades()
        assert len(lista) == 1
        assert lista[0]["id_vulnerabilidad"] == "VULN-001"
        assert lista[0]["nivel_riesgo"] == "MEDIO"

    def test_guardar_lote_duplicado(self):
        from database import guardar_lote_vulnerabilidades
        vulns = [
            {"id_vulnerabilidad": "V-1", "fuente_origen": "NVD"},
            {"id_vulnerabilidad": "V-1", "fuente_origen": "NVD"},
        ]
        insertados, errores = guardar_lote_vulnerabilidades(vulns)
        assert insertados == 2
        assert errores == 0

    def test_desactivar_vulnerabilidad(self):
        guardar_vulnerabilidad({"id_vulnerabilidad": "V-ACT", "fuente_origen": "TEST"})
        desactivar_vulnerabilidad("V-ACT")
        lista = listar_vulnerabilidades(activa=True)
        assert all(v["id_vulnerabilidad"] != "V-ACT" for v in lista)

    def test_stats_vulnerabilidades(self):
        from database import stats_vulnerabilidades, guardar_lote_vulnerabilidades
        guardar_lote_vulnerabilidades([
            {"id_vulnerabilidad": "V-A", "fuente_origen": "SRC1", "nivel_riesgo": "EXTREMO", "riesgo_valor": 25, "criticidad": 90.0},
            {"id_vulnerabilidad": "V-B", "fuente_origen": "SRC2", "nivel_riesgo": "BAJO", "riesgo_valor": 2, "criticidad": 10.0},
        ])
        sv = stats_vulnerabilidades()
        assert sv["total"] == 2
        assert sv["extremos"] == 1
        assert sv["bajos"] == 1
        assert sv["fuentes_distintas"] == 2

    def test_limpiar_antiguas(self):
        guardar_vulnerabilidad({"id_vulnerabilidad": "V-OLD", "fuente_origen": "TEST"})
        afectadas = limpiar_vulnerabilidades_antiguas(dias=0)
        assert afectadas >= 1


class TestAuditoria:
    def test_crear_y_obtener(self):
        aid = crear_auditoria("u1", sector="Salud", nombre_empresa="Test Corp")
        assert aid > 0

        auditorias = obtener_auditorias("u1")
        assert len(auditorias) == 1
        assert auditorias[0]["sector"] == "Salud"
        assert auditorias[0]["nombre_empresa"] == "Test Corp"

    def test_actualizar_auditoria(self):
        aid = crear_auditoria("u2")
        actualizar_auditoria(aid, etapa_actual="plan_mejora")
        aud = obtener_auditorias("u2")[0]
        assert aud["etapa_actual"] == "plan_mejora"
