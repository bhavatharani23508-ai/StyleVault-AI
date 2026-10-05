import streamlit as st

st.set_page_config(
    page_title="StyleVault AI",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database.database import (
    initialize_database,
    add_clothing,
    get_all_clothing,
    delete_clothing
)

initialize_database()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fffdfb 0%, #f8f7f5 100%);
}

[data-testid="stSidebar"] {
    background: #171717;
}

[data-testid="stSidebar"] * {
    color: #f7f7f7 !important;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    font-size: clamp(34px, 4vw, 52px);
    font-weight: 800;
    letter-spacing: -1.5px;
    margin-bottom: 6px;
}

.subtitle {
    font-size: 17px;
    color: #686868;
    margin-bottom: 28px;
}

.hero-card {
    padding: 30px;
    border-radius: 24px;
    border: 1px solid #e8e4df;
    background: linear-gradient(135deg, #ffffff, #f7f3ee);
    margin-bottom: 24px;
}

.feature-card {
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #e7e2dc;
    background: rgba(255,255,255,.92);
    min-height: 165px;
    margin-bottom: 18px;
    box-shadow: 0 8px 28px rgba(30,30,30,.045);
}

.feature-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 9px;
}

.feature-text {
    color: #666;
    font-size: 14px;
    line-height: 1.7;
}

.result-card {
    padding: 26px;
    border-radius: 22px;
    border: 1px solid #e5e1dc;
    background: #fff;
    box-shadow: 0 10px 30px rgba(0,0,0,.05);
    margin: 16px 0 22px;
}

.section-label {
    color: #777;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    font-weight: 700;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e7e2dc;
    border-radius: 18px;
    padding: 16px;
}

.stButton > button {
    border-radius: 12px;
    font-weight: 650;
    min-height: 42px;
}

div[data-testid="stChatMessage"] {
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("StyleVault AI")

    st.caption("Your Intelligent Wardrobe")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "My Wardrobe",
            "Add Clothing",
            "AI Stylist",
            "Smart Packing",
            "Wardrobe Analytics",
            "Style Chat"
        ]
    )

    st.divider()

    st.caption("AI Fashion Intelligence")
    st.caption("OCR • Computer Vision • LLM")


# =========================================================
# LOAD WARDROBE DATA
# =========================================================

wardrobe = get_all_clothing()


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Welcome to StyleVault AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your intelligent personal wardrobe and styling assistant.'
        '</div>',
        unsafe_allow_html=True
    )

    wardrobe = get_all_clothing()

    # =====================================================
    # EMPTY WARDROBE
    # =====================================================

    if not wardrobe:

        st.info(
            "Your wardrobe is empty. "
            "Go to 'Add Clothing' to add your first item."
        )

        st.divider()

        st.subheader("Start Building Your Digital Wardrobe")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-title">Digital Wardrobe</div>
                    <div class="feature-text">
                        Upload your clothes and let AI identify
                        clothing type, color, style, pattern and sleeve.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-title">AI Stylist</div>
                    <div class="feature-text">
                        Generate personalized outfit ideas using
                        only the clothes in your wardrobe.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-title">Smart Packing</div>
                    <div class="feature-text">
                        Create practical travel packing plans
                        from your existing wardrobe.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =====================================================
    # POPULATED WARDROBE
    # =====================================================

    else:

        total_items = len(wardrobe)

        categories = {}
        colors = {}
        styles = {}
        patterns = {}

        for item in wardrobe:

            clothing_type = item[1]
            color = item[2]
            style = item[3]
            pattern = item[4]

            if clothing_type:
                categories[clothing_type] = (
                    categories.get(clothing_type, 0) + 1
                )

            if color:
                colors[color] = (
                    colors.get(color, 0) + 1
                )

            if style:
                styles[style] = (
                    styles.get(style, 0) + 1
                )

            if pattern:
                patterns[pattern] = (
                    patterns.get(pattern, 0) + 1
                )

        top_category = (
            max(categories, key=categories.get)
            if categories else "Unknown"
        )

        top_color = (
            max(colors, key=colors.get)
            if colors else "Unknown"
        )

        top_style = (
            max(styles, key=styles.get)
            if styles else "Unknown"
        )

        # -------------------------------------------------
        # WARDROBE HEALTH SCORE
        # -------------------------------------------------

        score = 0

        if total_items >= 10:
            score += 30
        elif total_items >= 5:
            score += 20
        else:
            score += 10

        if len(categories) >= 5:
            score += 25
        elif len(categories) >= 3:
            score += 20
        elif len(categories) >= 2:
            score += 12
        else:
            score += 5

        if len(colors) >= 5:
            score += 25
        elif len(colors) >= 3:
            score += 20
        elif len(colors) >= 2:
            score += 12
        else:
            score += 5

        if len(styles) >= 3:
            score += 20
        elif len(styles) >= 2:
            score += 15
        elif len(styles) >= 1:
            score += 8

        score = min(score, 100)

        # =================================================
        # OVERVIEW
        # =================================================

        st.subheader("Wardrobe Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Wardrobe Items", total_items)

        with col2:
            st.metric("Categories", len(categories))

        with col3:
            st.metric("Top Color", top_color)

        with col4:
            st.metric("Top Style", top_style)

        st.divider()

        # =================================================
        # HEALTH + INSIGHT
        # =================================================

        col1, col2 = st.columns([1, 2])

        with col1:

            st.subheader("Wardrobe Health")

            st.metric(
                "Style Score",
                f"{score}/100"
            )

            st.progress(score / 100)

            if score >= 80:
                st.success("Excellent wardrobe variety.")
            elif score >= 60:
                st.info("Good foundation with room to improve.")
            else:
                st.warning("Add more variety to unlock more combinations.")

        with col2:

            st.subheader("AI Wardrobe Insight")

            if len(categories) <= 1:
                st.warning(
                    f"Your wardrobe is concentrated in "
                    f"{top_category}. Add other clothing categories "
                    f"to create more outfit combinations."
                )

            elif len(colors) <= 2:
                st.info(
                    f"{top_color} is one of your dominant colors. "
                    "Adding a few contrasting colors can increase "
                    "your styling options."
                )

            elif len(styles) <= 1:
                st.info(
                    f"Most of your wardrobe follows a "
                    f"{top_style} style. Adding another style "
                    "category can make your wardrobe more versatile."
                )

            else:
                st.success(
                    "Your wardrobe has a healthy mix of categories, "
                    "colors and styles."
                )

        st.divider()

        # =================================================
        # CATEGORY + COLOR BREAKDOWN
        # =================================================

        st.subheader("Wardrobe Breakdown")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Clothing Categories")

            for category, count in sorted(
                categories.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                st.write(
                    f"**{category}** — {count} item(s)"
                )

                st.progress(count / total_items)

        with col2:

            st.write("### Colors")

            for color, count in sorted(
                colors.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                st.write(
                    f"**{color}** — {count} item(s)"
                )

                st.progress(count / total_items)

        st.divider()

        # =================================================
        # RECENT ITEMS
        # =================================================

        st.subheader("Recently Added")

        recent_items = wardrobe[:4]

        cols = st.columns(len(recent_items))

        for col, item in zip(cols, recent_items):

            (
                item_id,
                clothing_type,
                color,
                style,
                pattern,
                sleeve,
                confidence,
                ocr_text,
                image_name,
                created_at
            ) = item

            with col:

                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="feature-title">
                            {color} {clothing_type}
                        </div>
                        <div class="feature-text">
                            <b>Style:</b> {style}<br>
                            <b>Pattern:</b> {pattern}<br>
                            <b>Sleeve:</b> {sleeve}<br>
                            <b>Confidence:</b> {confidence}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()

        # =================================================
        # AI FEATURES
        # =================================================

        st.subheader("StyleVault AI")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-title">AI Stylist</div>
                    <div class="feature-text">
                        Generate personalized outfits based on
                        occasion and your actual wardrobe.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-title">Smart Packing</div>
                    <div class="feature-text">
                        Build a practical travel wardrobe with
                        AI-generated packing combinations.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-title">Style Chat</div>
                    <div class="feature-text">
                        Ask natural-language questions about
                        outfits, colors and your wardrobe.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.caption(
            "StyleVault AI combines OCR, computer vision, "
            "SQLite wardrobe storage and a Hugging Face LLM."
        )


# =========================================================
# MY WARDROBE
# =========================================================

elif page == "My Wardrobe":

    st.title(
        "My Wardrobe"
    )

    st.write(
        "Your AI-powered digital wardrobe."
    )

    st.divider()

    wardrobe = get_all_clothing()

    if wardrobe:

        st.subheader(
            f"{len(wardrobe)} Clothing Item(s)"
        )

        for item in wardrobe:

            (
                item_id,
                clothing_type,
                color,
                style,
                pattern,
                sleeve,
                confidence,
                ocr_text,
                image_name,
                created_at
            ) = item

            with st.container(
                border=True
            ):

                col1, col2, col3 = st.columns(
                    [2, 2, 1]
                )

                with col1:

                    st.markdown(
                        f"### {color} {clothing_type}"
                    )

                    st.write(
                        f"**Style:** {style}"
                    )

                    st.write(
                        f"**Pattern:** {pattern}"
                    )

                with col2:

                    st.write(
                        f"**Sleeve:** {sleeve}"
                    )

                    st.write(
                        f"**AI Confidence:** "
                        f"{confidence}%"
                    )

                    if ocr_text:

                        st.write(
                            f"**Detected Text:** "
                            f"{ocr_text}"
                        )

                    else:

                        st.write(
                            "**Detected Text:** None"
                        )

                    st.caption(
                        f"Added: {created_at}"
                    )

                with col3:

                    if st.button(
                        "Delete",
                        key=f"delete_{item_id}"
                    ):

                        delete_clothing(
                            item_id
                        )

                        st.success(
                            "Item deleted."
                        )

                        st.rerun()

    else:

        st.info(
            "Your wardrobe is empty. "
            "Go to 'Add Clothing' to add your first item."
        )


# =========================================================
# ADD CLOTHING
# =========================================================

elif page == "Add Clothing":

    st.title("Add Clothing")
    st.write(
        "Build your digital wardrobe using AI Vision and OCR. "
        "Upload a clear clothing photo and StyleVault will identify "
        "its visual attributes and readable label information."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Clothing Image",
        type=["jpg", "jpeg", "png"],
        help="For best results, use a clear photo where the clothing item is visible."
    )

    if uploaded_file is not None:

        # Create a stable key for the current upload so repeated
        # Streamlit reruns do not create duplicate wardrobe entries.
        import hashlib

        file_bytes = uploaded_file.getvalue()
        file_key = hashlib.md5(file_bytes).hexdigest()

        preview_col, info_col = st.columns([1.35, 1])

        with preview_col:
            st.image(
                file_bytes,
                caption="Uploaded Clothing",
                use_container_width=True
            )

        with info_col:
            st.subheader("Upload Details")
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
            st.write("**Analysis:** AI Vision + OCR")

            st.info(
                "Tip: A well-lit image with the garment clearly visible "
                "gives better classification results."
            )

        st.divider()

        if st.button(
            "Analyze Clothing",
            type="primary",
            use_container_width=True
        ):

            try:

                from modules.clothing_analyzer import analyze_clothing
                from modules.ocr_engine import extract_text

                # -------------------------------------------------
                # AI VISION
                # -------------------------------------------------

                with st.status(
                    "Analyzing clothing with AI...",
                    expanded=True
                ) as analysis_status:

                    st.write("Detecting clothing type, color and style...")

                    uploaded_file.seek(0)
                    clothing_result = analyze_clothing(uploaded_file)

                    st.write("Scanning visible labels and text...")

                    uploaded_file.seek(0)
                    ocr_result = extract_text(uploaded_file)

                    analysis_status.update(
                        label="Analysis completed",
                        state="complete",
                        expanded=False
                    )

                # -------------------------------------------------
                # NORMALIZE RESULTS
                # -------------------------------------------------

                clothing_result = clothing_result or {}
                ocr_result = ocr_result or []

                ocr_text = " ".join(
                    str(item.get("text", "")).strip()
                    for item in ocr_result
                    if item.get("text")
                ).strip()

                result = {
                    "clothing_type": clothing_result.get(
                        "clothing_type", "Unknown"
                    ),
                    "color": clothing_result.get(
                        "color", "Unknown"
                    ),
                    "style": clothing_result.get(
                        "style", "Unknown"
                    ),
                    "pattern": clothing_result.get(
                        "pattern", "Unknown"
                    ),
                    "sleeve": clothing_result.get(
                        "sleeve", "Unknown"
                    ),
                    "clothing_confidence": clothing_result.get(
                        "clothing_confidence", 0
                    ),
                    "style_confidence": clothing_result.get(
                        "style_confidence", 0
                    ),
                    "pattern_confidence": clothing_result.get(
                        "pattern_confidence", 0
                    ),
                    "ocr_text": ocr_text,
                    "ocr_result": ocr_result,
                    "file_name": uploaded_file.name,
                    "file_key": file_key
                }

                # Persist analysis across Streamlit reruns.
                st.session_state["last_clothing_analysis"] = result

                # -------------------------------------------------
                # SAVE ONLY ONCE FOR THIS EXACT IMAGE
                # -------------------------------------------------

                if st.session_state.get("last_saved_clothing_key") != file_key:

                    add_clothing(
                        clothing_type=result["clothing_type"],
                        color=result["color"],
                        style=result["style"],
                        pattern=result["pattern"],
                        sleeve=result["sleeve"],
                        confidence=result["clothing_confidence"],
                        ocr_text=result["ocr_text"],
                        image_name=result["file_name"]
                    )

                    st.session_state["last_saved_clothing_key"] = file_key
                    st.session_state["last_saved_clothing_message"] = (
                        "New clothing item added to your wardrobe."
                    )

                else:
                    st.session_state["last_saved_clothing_message"] = (
                        "This clothing item is already saved in your wardrobe."
                    )

            except ImportError as e:

                st.error("Required AI module was not found.")

                st.code(str(e))

                st.info(
                    "Make sure these files exist:\n\n"
                    "modules/clothing_analyzer.py\n"
                    "modules/ocr_engine.py\n"
                    "database/database.py"
                )

            except Exception as e:

                st.error("Unable to analyze the clothing image.")
                st.code(str(e))

        # ---------------------------------------------------------
        # DISPLAY LAST ANALYSIS
        # ---------------------------------------------------------

        result = st.session_state.get("last_clothing_analysis")

        if result and result.get("file_key") == file_key:

            saved_message = st.session_state.get(
                "last_saved_clothing_message"
            )

            if saved_message:
                st.success(saved_message)

            st.divider()

            st.subheader("AI Clothing Profile")

            # Main attributes
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Type",
                    str(result["clothing_type"]).title()
                )

            with col2:
                st.metric(
                    "Color",
                    str(result["color"]).title()
                )

            with col3:
                st.metric(
                    "Style",
                    str(result["style"]).title()
                )

            with col4:
                st.metric(
                    "Pattern",
                    str(result["pattern"]).title()
                )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Sleeve",
                    str(result["sleeve"]).title()
                )

            with col2:
                try:
                    clothing_confidence = float(
                        result["clothing_confidence"]
                    )
                except (TypeError, ValueError):
                    clothing_confidence = 0

                st.metric(
                    "AI Confidence",
                    f"{clothing_confidence:.1f}%"
                )

            with col3:
                st.metric(
                    "OCR Text",
                    "Detected" if result["ocr_text"] else "None"
                )

            st.divider()

            # Confidence breakdown
            st.subheader("AI Confidence Breakdown")

            confidence_data = [
                (
                    "Clothing Classification",
                    result["clothing_confidence"]
                ),
                (
                    "Style Classification",
                    result["style_confidence"]
                ),
                (
                    "Pattern Classification",
                    result["pattern_confidence"]
                )
            ]

            for label, value in confidence_data:

                try:
                    confidence_value = float(value)
                except (TypeError, ValueError):
                    confidence_value = 0

                confidence_value = max(
                    0,
                    min(100, confidence_value)
                )

                st.write(
                    f"**{label}: {confidence_value:.1f}%**"
                )

                st.progress(
                    confidence_value / 100
                )

            st.divider()

            # OCR section
            st.subheader("OCR / Clothing Label Intelligence")

            if result["ocr_result"]:

                st.success(
                    "Readable text was detected from the uploaded image."
                )

                for index, item in enumerate(
                    result["ocr_result"],
                    start=1
                ):

                    text_value = str(
                        item.get("text", "")
                    ).strip()

                    if not text_value:
                        continue

                    confidence_value = item.get(
                        "confidence",
                        0
                    )

                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(
                            f"**{index}.** {text_value}"
                        )

                    with col2:
                        st.caption(
                            f"Confidence: {confidence_value}"
                        )

                with st.expander("View combined OCR text"):
                    st.code(
                        result["ocr_text"] or "No text detected."
                    )

            else:

                st.info(
                    "No readable brand, size, material or label "
                    "text was detected in this image."
                )

            st.divider()

            # Human-readable summary
            st.subheader("StyleVault Summary")

            clothing_type = result["clothing_type"]
            color = result["color"]
            style = result["style"]
            pattern = result["pattern"]
            sleeve = result["sleeve"]

            st.write(
                f"This item is classified as a **{color} "
                f"{clothing_type}** with a **{pattern}** pattern. "
                f"It has a **{sleeve}** sleeve style and an overall "
                f"**{style}** style classification."
            )

            st.caption(
                "The profile is generated from computer vision "
                "classification and OCR. Predictions may vary with "
                "image quality, lighting and garment visibility."
            )

            st.divider()

            # Reset analysis
            if st.button(
                "Clear Analysis",
                use_container_width=True
            ):
                st.session_state.pop(
                    "last_clothing_analysis",
                    None
                )
                st.session_state.pop(
                    "last_saved_clothing_message",
                    None
                )
                st.rerun()

    else:

        st.info(
            "Upload a clothing image to begin your wardrobe analysis."
        )

        st.markdown(
            """
            **Best results**
            - Use a clear, well-lit clothing photo.
            - Keep the garment fully visible.
            - Avoid heavy blur or extreme shadows.
            - Include the label if you want OCR to read it.
            """
        )


# =========================================================
# AI STYLIST
# =========================================================

elif page == "AI Stylist":

    st.markdown('<div class="main-title">AI Stylist</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Create a personalized outfit using the clothes you already own.</div>', unsafe_allow_html=True)

    wardrobe = get_all_clothing()

    if not wardrobe:
        st.warning("Your wardrobe is empty.")
        st.info("Go to Add Clothing and add some clothes before using AI Stylist.")
    else:
        from modules.stylist_engine import generate_outfit

        st.markdown('<div class="section-label">Outfit preferences</div>', unsafe_allow_html=True)
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            occasion = st.selectbox("Occasion", ["College", "Casual", "Party", "Interview", "Travel", "Date", "Traditional"], key="stylist_occasion")
        with col2:
            preference = st.selectbox("Style Preference", ["Comfortable", "Minimal", "Trendy", "Formal", "Casual"], key="stylist_preference")

        extra_preference = st.text_input("Extra preference", placeholder="Example: Keep it simple and comfortable", key="stylist_extra_preference")

        if st.button("Generate AI Outfit", type="primary", use_container_width=True, key="generate_stylist_outfit"):
            try:
                with st.status("StyleVault AI is creating your outfit...", expanded=True) as status:
                    st.write("Checking your wardrobe...")
                    st.write("Matching clothing with your preferences...")
                    result = generate_outfit(wardrobe, occasion, preference)
                    status.update(label="Outfit generated", state="complete", expanded=False)
                st.session_state["last_stylist_result"] = result
                st.session_state["last_stylist_extra_preference"] = extra_preference
                st.session_state["last_stylist_occasion"] = occasion
                st.session_state["last_stylist_preference"] = preference
            except ImportError as e:
                st.error("AI Stylist module was not found.")
                st.code(str(e))
            except Exception as e:
                st.error("Something went wrong while creating the outfit.")
                st.code(str(e))

        result = st.session_state.get("last_stylist_result")
        if result:
            st.divider()
            if result.get("status") == "success":
                saved_occasion = st.session_state.get("last_stylist_occasion", occasion)
                saved_preference = st.session_state.get("last_stylist_preference", preference)
                st.subheader("Your AI-Generated Outfit")
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Occasion", saved_occasion)
                with c2: st.metric("Style", saved_preference)
                with c3: st.metric("Wardrobe Used", len(wardrobe))
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(result.get("response", "No outfit response was generated."))
                st.markdown('</div>', unsafe_allow_html=True)
                saved_extra = st.session_state.get("last_stylist_extra_preference", "")
                if saved_extra:
                    st.caption(f"Additional preference: {saved_extra}")
                st.success("Outfit generated from your StyleVault wardrobe.")
            elif result.get("status") == "empty":
                st.warning(result.get("message", "Your wardrobe is empty."))
            else:
                st.error("The AI Stylist could not generate an outfit.")
                st.code(result.get("message", "Unknown error occurred."))

            if st.button("Clear Outfit", use_container_width=True, key="clear_stylist_result"):
                for key in ["last_stylist_result", "last_stylist_extra_preference", "last_stylist_occasion", "last_stylist_preference"]:
                    st.session_state.pop(key, None)
                st.rerun()


# =========================================================
# SMART PACKING
# =========================================================

elif page == "Smart Packing":

    st.markdown('<div class="main-title">Smart Packing</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Build a practical travel wardrobe from your existing clothes.</div>', unsafe_allow_html=True)

    wardrobe = get_all_clothing()

    if not wardrobe:
        st.warning("Your wardrobe is empty.")
        st.info("Go to Add Clothing and add some clothes before creating a packing plan.")
    else:
        from modules.packing_engine import generate_packing_plan

        st.markdown('<div class="section-label">Trip details</div>', unsafe_allow_html=True)
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            destination = st.text_input("Destination", placeholder="Example: Chennai", key="packing_destination")
        with col2:
            days = st.number_input("Number of Days", min_value=1, max_value=30, value=3, step=1, key="packing_days")
        purpose = st.selectbox("Trip Purpose", ["Vacation", "College", "Business", "Wedding", "Casual Trip"], key="packing_purpose")

        if st.button("Generate AI Packing Plan", type="primary", use_container_width=True, key="generate_packing_plan"):
            if not destination.strip():
                st.warning("Please enter a destination.")
            else:
                try:
                    with st.status("StyleVault AI is creating your packing plan...", expanded=True) as status:
                        st.write("Checking your wardrobe...")
                        st.write("Matching clothing with your trip...")
                        result = generate_packing_plan(wardrobe, destination.strip(), int(days), purpose)
                        status.update(label="Packing plan generated", state="complete", expanded=False)
                    st.session_state["last_packing_result"] = result
                    st.session_state["last_packing_destination"] = destination.strip()
                    st.session_state["last_packing_days"] = int(days)
                    st.session_state["last_packing_purpose"] = purpose
                except ImportError as e:
                    st.error("AI Packing module was not found.")
                    st.code(str(e))
                except Exception as e:
                    st.error("Something went wrong while creating the packing plan.")
                    st.code(str(e))

        result = st.session_state.get("last_packing_result")
        if result:
            st.divider()
            if result.get("status") == "success":
                saved_destination = st.session_state.get("last_packing_destination", destination)
                saved_days = st.session_state.get("last_packing_days", days)
                saved_purpose = st.session_state.get("last_packing_purpose", purpose)
                st.subheader("Your AI Packing Plan")
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Destination", saved_destination)
                with c2: st.metric("Duration", f"{saved_days} day(s)")
                with c3: st.metric("Purpose", saved_purpose)
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(result.get("response", "No packing plan was generated."))
                st.markdown('</div>', unsafe_allow_html=True)
                st.success("Packing plan generated using your StyleVault wardrobe.")
            elif result.get("status") == "empty":
                st.warning(result.get("message", "Your wardrobe is empty."))
            else:
                st.error("The AI Packing Assistant could not generate a plan.")
                st.code(result.get("message", "Unknown error occurred."))

            if st.button("Clear Packing Plan", use_container_width=True, key="clear_packing_plan"):
                for key in ["last_packing_result", "last_packing_destination", "last_packing_days", "last_packing_purpose"]:
                    st.session_state.pop(key, None)
                st.rerun()


# =========================================================
# WARDROBE ANALYTICS
# =========================================================

elif page == "Wardrobe Analytics":

    st.title("Wardrobe Analytics")

    st.write(
        "Understand your wardrobe through clothing, color, "
        "style and pattern insights."
    )

    st.divider()

    wardrobe = get_all_clothing()

    if not wardrobe:

        st.info(
            "Analytics will become available after "
            "clothing items are added."
        )

    else:

        total_items = len(wardrobe)

        # =================================================
        # COLLECT DATA
        # =================================================

        category_counts = {}
        color_counts = {}
        style_counts = {}
        pattern_counts = {}
        sleeve_counts = {}

        for item in wardrobe:

            clothing_type = item[1]
            color = item[2]
            style = item[3]
            pattern = item[4]
            sleeve = item[5]

            if clothing_type:
                category_counts[clothing_type] = (
                    category_counts.get(clothing_type, 0) + 1
                )

            if color:
                color_counts[color] = (
                    color_counts.get(color, 0) + 1
                )

            if style:
                style_counts[style] = (
                    style_counts.get(style, 0) + 1
                )

            if pattern:
                pattern_counts[pattern] = (
                    pattern_counts.get(pattern, 0) + 1
                )

            if sleeve:
                sleeve_counts[sleeve] = (
                    sleeve_counts.get(sleeve, 0) + 1
                )

        # =================================================
        # TOP METRICS
        # =================================================

        most_common_category = (
            max(category_counts, key=category_counts.get)
            if category_counts else "-"
        )

        most_common_color = (
            max(color_counts, key=color_counts.get)
            if color_counts else "-"
        )

        most_common_style = (
            max(style_counts, key=style_counts.get)
            if style_counts else "-"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Items",
                total_items
            )

        with col2:
            st.metric(
                "Top Category",
                most_common_category
            )

        with col3:
            st.metric(
                "Top Color",
                most_common_color
            )

        with col4:
            st.metric(
                "Top Style",
                most_common_style
            )

        st.divider()

        # =================================================
        # CATEGORY DISTRIBUTION
        # =================================================

        st.subheader("Clothing Distribution")

        if category_counts:

            for category, count in sorted(
                category_counts.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                percentage = (count / total_items) * 100

                st.write(
                    f"**{category}** — "
                    f"{count} item(s) "
                    f"({percentage:.1f}%)"
                )

                st.progress(
                    count / total_items
                )

        st.divider()

        # =================================================
        # COLOR + STYLE
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Color Distribution")

            if color_counts:

                for color, count in sorted(
                    color_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):

                    st.write(
                        f"**{color}** — {count}"
                    )

            else:

                st.write("No color information available.")

        with col2:

            st.subheader("Style Distribution")

            if style_counts:

                for style, count in sorted(
                    style_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):

                    st.write(
                        f"**{style}** — {count}"
                    )

            else:

                st.write("No style information available.")

        st.divider()

        # =================================================
        # PATTERN + SLEEVE
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Pattern Analysis")

            if pattern_counts:

                for pattern, count in sorted(
                    pattern_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):

                    st.write(
                        f"**{pattern}** — {count}"
                    )

            else:

                st.write("No pattern information available.")

        with col2:

            st.subheader("Sleeve Analysis")

            if sleeve_counts:

                for sleeve, count in sorted(
                    sleeve_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):

                    st.write(
                        f"**{sleeve}** — {count}"
                    )

            else:

                st.write("No sleeve information available.")

        st.divider()

        # =================================================
        # WARDROBE INSIGHTS
        # =================================================

        st.subheader("Wardrobe Insights")

        if category_counts:

            top_category_count = max(
                category_counts.values()
            )

            top_category_percentage = (
                top_category_count / total_items
            ) * 100

            if top_category_percentage >= 50:

                st.warning(
                    f"Your wardrobe is heavily focused on "
                    f"{most_common_category}. Consider adding "
                    f"more variety to your clothing collection."
                )

            else:

                st.success(
                    "Your wardrobe has a reasonably balanced "
                    "distribution of clothing categories."
                )

        if color_counts:

            top_color_count = max(
                color_counts.values()
            )

            top_color_percentage = (
                top_color_count / total_items
            ) * 100

            if top_color_percentage >= 50:

                st.info(
                    f"{most_common_color} is your dominant color. "
                    f"Adding contrasting colors could create "
                    f"more outfit combinations."
                )

            else:

                st.success(
                    "Your wardrobe contains a good variety "
                    "of colors."
                )

        st.caption(
            "Analytics are generated from your StyleVault "
            "wardrobe data."
        )


# =========================================================
# STYLE CHAT
# =========================================================

elif page == "Style Chat":

    st.title(
        "StyleVault AI Chat"
    )

    st.write(
        "Ask questions about your wardrobe and outfits."
    )

    st.divider()

    # -----------------------------------------------------
    # LOAD CHAT ENGINE
    # -----------------------------------------------------

    from modules.chat_engine import (
        chat_with_wardrobe
    )

    # -----------------------------------------------------
    # CHAT HISTORY
    # -----------------------------------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # -----------------------------------------------------
    # DISPLAY PREVIOUS MESSAGES
    # -----------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # -----------------------------------------------------
    # USER QUESTION
    # -----------------------------------------------------

    question = st.chat_input(
        "Ask something like: "
        "What can I wear with black jeans?"
    )

    if question:

        # -------------------------------------------------
        # DISPLAY USER MESSAGE
        # -------------------------------------------------

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        # -------------------------------------------------
        # GENERATE AI RESPONSE
        # -------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "StyleVault AI is thinking..."
            ):

                wardrobe = get_all_clothing()

                answer = chat_with_wardrobe(
                    wardrobe,
                    question,
                    st.session_state.chat_history
                )

            st.markdown(
                answer
            )

        # -------------------------------------------------
        # SAVE AI RESPONSE
        # -------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    # -----------------------------------------------------
    # CLEAR CHAT
    # -----------------------------------------------------

    if st.session_state.chat_history:

        st.divider()

        if st.button(
            "Clear Chat"
        ):

            st.session_state.chat_history = []

            st.rerun()