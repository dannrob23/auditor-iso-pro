from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 📊 Dashboard Consolidado 360° (Cumplimiento, Madurez y Riesgos)")
    
    sg = stats_globales()
    sv = stats_vulnerabilidades()
    total_r = sg.get("total_reportes") or 0
    total_v = sv.get("total") or 0
    
    nivel_madurez = "No evaluado"
    pct_madurez = 0.0
    if st.session_state.get("auto_resultados"):
        nivel_madurez = st.session_state["auto_resultados"].get("nivel_global", "No evaluado")
        pct_madurez = st.session_state["auto_resultados"].get("porcentaje_global", 0.0)

    c1, c2, c3, c4 = st.columns(4)
    def metric_html(val, label, color="#a78bfa"):
        return f"<div class='metric-box'><div class='metric-value' style='color:{color}'>{val}</div><div class='metric-label'>{label}</div></div>"
    
    c1.markdown(metric_html(total_r, "Políticas Auditadas", "#a78bfa"), unsafe_allow_html=True)
    c2.markdown(metric_html(f"{(sg.get('avg_cumplimiento') or 0.0):.1f}%", "Cumplimiento Promedio (Gap)", "#34d399"), unsafe_allow_html=True)
    c3.markdown(metric_html(f"{pct_madurez:.1f}%" if pct_madurez > 0 else "N/A", f"Madurez: {nivel_madurez}", "#60a5fa"), unsafe_allow_html=True)
    c4.markdown(metric_html(total_v, "Vulnerabilidades IA Activas", "#fb923c" if total_v > 0 else "#34d399"), unsafe_allow_html=True)

    st.markdown("---")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        if total_r == 0:
            st.info("Aún no hay análisis de confluencia. Sube un documento en 'Auditoría de IA' para ver gráficos.")
        else:
            conformes_t    = sg.get("total_conformes", 0) or 0
            parciales_t    = sg.get("total_parciales", 0) or 0
            no_conformes_t = sg.get("total_no_conformes", 0) or 0
            fig_donut = go.Figure(go.Pie(
                labels=["✅ Conformes", "⚠️ Parciales", "❌ No Conformes"],
                values=[conformes_t, parciales_t, no_conformes_t],
                hole=0.55,
                marker_colors=["#059669", "#d97706", "#dc2626"],
                textfont_size=12,
            ))
            fig_donut.update_layout(
                title="Distribución global de controles (Auditoría)",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="white", showlegend=True,
                legend=dict(orientation="h", y=-0.15),
                height=320,
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    with col_g2:
        if total_v == 0:
            st.info("No hay vulnerabilidades IA en la base de datos. Actualiza la base en 'Matriz Riesgos IA' para ver estadísticas.")
        else:
            extremos = sv.get("extremos") or 0
            altos = sv.get("altos") or 0
            medios = sv.get("medios") or 0
            bajos = sv.get("bajos") or 0
            
            fig_bar_vuln = go.Figure(go.Bar(
                x=["Extremo", "Alto", "Medio", "Bajo"],
                y=[extremos, altos, medios, bajos],
                marker_color=["#ef4444", "#f97316", "#eab308", "#10b981"],
                text=[str(v) for v in [extremos, altos, medios, bajos]],
                textposition="outside",
            ))
            fig_bar_vuln.update_layout(
                title="Vulnerabilidades de IA por Nivel de Riesgo",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="white", yaxis_range=[0, max(extremos, altos, medios, bajos) * 1.2 + 2],
                height=320,
            )
            st.plotly_chart(fig_bar_vuln, use_container_width=True)

    st.markdown("---")
    col_g3, col_g4 = st.columns(2)
    
    with col_g3:
        if total_r > 0:
            reportes = listar_reportes(10)
            if reportes:
                reportes_cron = sorted(reportes, key=lambda x: x.get("created_at", ""))
                fechas = [r["created_at"][:16].replace("T", " ") for r in reportes_cron]
                pcts = [r["cumplimiento_pct"] for r in reportes_cron]
                nombres = [r["nombre_doc"][:20] for r in reportes_cron]
                
                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(
                    x=fechas,
                    y=pcts,
                    mode='lines+markers',
                    name='Cumplimiento',
                    line=dict(color='#8b5cf6', width=3),
                    marker=dict(size=8, color='#34d399', symbol='circle'),
                    text=[f"{n} ({p}%)" for n, p in zip(nombres, pcts)],
                    hoverinfo='text+x'
                ))
                fig_line.update_layout(
                    title="Tendencia Temporal de Cumplimiento (Últimos 10 Análisis)",
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white", yaxis_range=[0, 110],
                    xaxis_tickangle=-30, height=320,
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig_line, use_container_width=True)
                
    with col_g4:
        if pct_madurez > 0:
            res = st.session_state["auto_resultados"]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[res["dimensiones"][d]["porcentaje"] for d in res["dimensiones"]],
                theta=list(res["dimensiones"].keys()),
                fill='toself',
                name='Madurez IA-SEC',
                line_color='#7c3aed'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                title="Madurez Organizacional por Dimensión",
                height=320
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("Completa el cuestionario en 'Autodiagnóstico' para habilitar el gráfico radar de madurez organizacional.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Historial ─────────────────────────────────────────────────────────────
