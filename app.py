    tw_status_html = "";
    if show_tw:
        tw_status_html = ("<span style='font-size:0.68rem;color:#454550;'>TW "
               "<span style='color:#39e5b6;font-family:DM Mono,monospace;'>" + str(ra.get('tw_status','')) + "</span></span>");

    st.markdown(f"{tw_status_html}")