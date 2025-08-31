system_prompt = "You are a computer vision and natural language processing (multi-modal) agent."

checklist_prompt = """
    Considering these 4 images as an example, imagine that a product must follow this standard. Could you provide a list of possible alterations, defects and anomalies that could be present in the product? Provide this list in short sentences.
"""
text_prompts = {
    1: "Do you see any possible adulterations change, defect or anomaly on the product?",
    2: """
            Given the following product description that represents the normal and expected apperance on a production line:
            {}
            Do you see any possible adulterations change, defect or anomaly on the product?
        """,
    3: """
        PART 1 – Normal product specification
            Reference description:
            {}
            Treat every characteristic in this paragraph as a quality requirement.
        
        PART 2 – Visual comparison task
            Reference images: The first four images show compliant (good) units that match the specification above.
            Test image: The fifth image shows another unit from the same production line.
            Your task:
        
            1. Compare the test image against each of the four reference images and against the written specification from PART 1.
        
            2. State whether the test image exhibits any adulterations, changes, defects, or anomalies.
        
            3. If you detect a deviation, describe exactly what differs and where it appears.
        
            4. If no significant deviation exists, reply: 'No anomaly detected.'
            
            Evaluate both the product body and its packaging.
        """,
    4: """
        PART 1 – Normal product specification
            Reference description:
            {}
            Treat every characteristic in this paragraph as a quality requirement.
        
        PART 2 – Anomaly checklist  
            Checklist items (expected to be absent from a defect‑free unit):  
            {}  
            During evaluation, treat the appearance of any checklist item as evidence of a potential anomaly.
        
        
        PART 3 – Visual comparison task
            Reference images: The first four images show compliant (good) units that match the specification above.
            Test image: The fifth image shows another unit from the same production line.
            Your task:
        
            1. Compare the test image against each of the four reference images and against the written specification from PART 1 and the checklist in PART 2.
        
            2. State whether the test image exhibits any adulterations, changes, defects, or anomalies.
        
            3. If you detect a deviation, describe exactly what differs and where it appears.
        
            4. If no significant deviation exists, reply: 'No anomaly detected.'
        
            Evaluate both the product body and its packaging.
        """,
    5: """
        PART 1 – Normal product specification
            Reference description:
            {}
            Treat every characteristic in this paragraph as a quality requirement.
        
        PART 2 – Anomaly checklist  
            Checklist items (expected to be absent from a defect‑free unit):  
            {}  
            During evaluation, treat the appearance of any checklist item as evidence of a potential anomaly.
        
        
        PART 3 – Visual comparison task
            Reference images: The first four images show compliant (good) units that match the specification above.
            Test image: The fifth image shows another unit from the same production line.
            Your task:
        
            1. Compare the test image against each of the four reference images and against the written specification from PART 1 and the checklist in PART 2.
        
            2. State whether the test image exhibits any adulterations, changes, defects, or anomalies.
        
            3. If you detect a deviation, describe exactly what differs and where it appears.
        
            4. If no significant deviation exists, reply: 'No anomaly detected.'
        
            Evaluate both the product body and its packaging.
        """,
    6:"""Look at the first {} images, imagine that it is an industrial product that must follow this standard, is there a problem with the last image?""",
    7:"""
        PART 1 – Normal product specification
            Reference description:
            {}
        
        PART 2 – Anomaly checklist  
            Checklist:  
            {}  
        
        PART 3 - Image analysis
            Compare the test image against each of the the written specification from PART 1 and the checklist in PART 2.
            Do you see any possible adulterations change, defect or anomaly on the product?
    """
}

anomaly_list = {
    "breakfast_box": [
        "missing almonds",
        "missing bananas",
        "missing toppings",
        "missing cereals",
        "missing cereals and toppings",
        "2 nectarines 1 tangerine",
        "1 nectarine 1 tangerine",
        "0 nectarines 2 tangerines",
        "0 nectarines 3 tangerines",
        "3 nectarines 0 tangerines",
        "0 nectarines 1 tangerine",
        "0 nectarines 0 tangerines",
        "0 nectarines 4 tangerines",
        "compartments swapped",
        "overflow",
        "underflow",
        "wrong ratio",
        "mixed cereals",
        "fruit damaged",
        "box damaged",
        "toppings crushed",
        "contamination"
    ],

    "juice_bottle": [
        "missing top label",
        "missing bottom label",
        "swapped labels",
        "damaged label",
        "rotated label",
        "misplaced label top",
        "misplaced label bottom",
        "label text incomplete",
        "empty bottle",
        "wrong fill level too much",
        "wrong fill level not enough",
        "misplaced fruit icon",
        "missing fruit icon",
        "unknown fruit icon",
        "incomplete fruit icon",
        "wrong juice type",
        "juice color",
        "contamination"
    ],

    "pushpins": [
        "1 additional pushpin",
        "2 additional pushpins",
        "missing pushpin",
        "missing separator",
        "front bent",
        "broken",
        "color",
        "contamination"
    ],

    "screw_bag": [
        "screw too long",
        "screw too short",
        "1 very short screw",
        "2 very short screws",
        "1 additional long screw",
        "1 additional short screw",
        "1 additional nut",
        "2 additional nuts",
        "1 additional washer",
        "2 additional washers",
        "1 missing long screw",
        "1 missing short screw",
        "1 missing nut",
        "2 missing nuts",
        "1 missing washer",
        "2 missing washers",
        "bag broken",
        "color",
        "contamination",
        "part broken"
    ],

    "splicing_connectors": [
        "wrong connector type 5 2",
        "wrong connector type 5 3",
        "wrong connector type 3 2",
        "cable too short T2",
        "cable too short T3",
        "cable too short T5",
        "missing connector",
        "missing connector and cable",
        "missing cable",
        "extra cable",
        "cable color",
        "broken cable",
        "cable cut",
        "cable not plugged",
        "unknown cable color",
        "wrong cable location",
        "flipped connector",
        "broken connector",
        "open lever",
        "color",
        "contamination"
    ],

    "bottle": [
        "broken_large",
        "broken_small",
        "contamination"
    ],

    "cable": [
        "bent_wire",
        "cable_swap",
        "combined",
        "cut_inner_insulation",
        "cut_outer_insulation",
        "missing_cable",
        "missing_wire",
        "poke_insulation"
    ],

    "capsule": [
        "crack",
        "faulty_imprint",
        "poke",
        "scratch",
        "squeeze"
    ],

    "carpet": [
        "color",
        "cut",
        "hole",
        "metal_contamination",
        "thread"
    ],

    "grid": [
        "bent",
        "broken",
        "glue",
        "metal_contamination",
        "thread"
    ],

    "hazelnut": [
        "crack",
        "cut",
        "hole",
        "print"
    ],

    "leather": [
        "color",
        "cut",
        "fold",
        "glue",
        "poke"
    ],

    "metal_nut": [
        "bent",
        "color",
        "flip",
        "scratch"
    ],

    "pill": [
        "color",
        "combined",
        "contamination",
        "crack",
        "faulty_imprint",
        "pill_type",
        "scratch"
    ],

    "screw": [
        "manipulated_front",
        "scratch_head",
        "scratch_neck",
        "thread_side",
        "thread_top"
    ],

    "tile": [
        "crack",
        "glue_strip",
        "gray_stroke",
        "oil",
        "rough"
    ],

    "toothbrush": [
        "defective"
    ],

    "transistor": [
        "bent_lead",
        "cut_lead",
        "damaged_case",
        "misplaced"
    ],

    "wood": [
        "color",
        "combined",
        "hole",
        "liquid",
        "scratch"
    ],

    "zipper": [
        "broken_teeth",
        "combined",
        "fabric_border",
        "fabric_interior",
        "rough",
        "split_teeth",
        "squeezed_teeth"
    ]
}

objects_description = {
    "breakfast_box": """
This product is a pre-packaged, healthy snack or light meal, presented in a disposable, off-white, rectangular container with rounded corners. The container is made of a fibrous, possibly biodegradable material (like pressed paper or bagasse) and is divided into two compartments by a gently curved, raised partition.

**Container:**
*   **Size:** Appears to be a single-serving size, typical for a to-go meal.
*   **Color:** Off-white or light cream.
*   **Proportions:** The container is wider than it is tall. It is divided into two unequal compartments. The left compartment is smaller, occupying roughly 35-40% of the total width, while the right compartment is larger, taking up the remaining 60-65%.

**Left Compartment (Fresh Fruit):**
*   **Location:** Occupies the smaller, left-hand section of the container.
*   **Amount:** Contains three pieces of whole fruit, stacked vertically.
*   **Contents & Color:**
    *   **Two Citrus Fruits:** These are small, round, and intensely orange, characteristic of mandarins, clementines, or small tangerines. They have a slightly dimpled skin texture. Their diameter appears to be approximately 2 to 2.5 inches.
    *   **One Stone Fruit:** This is a larger, more spherical fruit, likely a peach or nectarine. Its color is a variegated blend of deep red, blushing into orange and pale yellow patches. It has a visible indentation or cleft. Its diameter is slightly larger than the citrus fruits, perhaps 2.5 to 3 inches.
*   **Arrangement:** The three fruits fit snugly within this compartment, usually arranged in a vertical line. The relative position of the peach/nectarine (top, middle, or bottom) varies slightly across the images but it consistently takes up the most individual space.
*   **Proportions:** The fruits fill the height of this compartment almost completely.

**Right Compartment (Granola and Nut/Dried Fruit Mix):**
*   **Location:** Occupies the larger, right-hand section of the container.
*   **Amount:** This compartment is generously filled with a mixture of ingredients.
*   **Contents & Color:**
    *   **Granola:** This is the most voluminous component, filling the top two-thirds to three-quarters of this compartment. It consists of toasted, golden-brown oat clusters and individual rolled oats, with varying shades from light tan to medium brown, indicating a good toasting.
    *   **Almonds:** Located primarily in the lower quarter to one-third of this compartment, mixed with dried banana chips. These are whole, unblanched (skin-on) almonds, medium brown in color. They are typically about 0.75 to 1 inch in length. There appears to be a substantial handful, perhaps 15-25 almonds.
    *   **Dried Banana Chips:** Interspersed with the almonds at the bottom of the compartment. These are circular, light beige to pale yellow slices of dried banana, often with a slightly darker, brownish center where the seeds would have been. Each chip is roughly 1 to 1.5 inches in diameter.
*   **Proportions within the compartment:**
    *   Granola constitutes the largest portion, roughly 65-75% of the volume in this section.
    *   The remaining 25-35% is a mix of almonds and banana chips, which appear to be in roughly similar quantities by visual bulk, though the banana chips might be slightly more voluminous due to their shape.

**Overall Proportions and Presentation:**
*   The meal is designed for convenience, with distinct components separated.
*   The fruit side offers fresh, vibrant colors, while the granola side offers a more textured, earthy-toned appeal.
*   By volume, the granola and its accompanying mix appear to be slightly more substantial than the whole fruits.
*   The entire product is presented from an overhead (top-down) perspective against a dark, almost black background, which makes the off-white container and its colorful contents stand out.
""",

    "juice_bottle": """
This product is presented as a single, small, clear glass bottle, showcased against a plain black background. The bottle is designed for a single serving of juice.

**Object: Bottle**
*   **Size & Proportions:** The bottle is relatively small and slender. Its overall height can be estimated to be roughly 4-5 times its width at the base. The neck of the bottle comprises about one-quarter to one-third of its total height. The main body is significantly wider than the neck.
*   **Shape:** The bottle has a rectangular base with flat front and back surfaces and slightly rounded side edges. This rectangular body transitions smoothly into a narrower, cylindrical neck. The top of the neck features visible screw threads, indicating it's designed for a screw-on cap (which is not present in the images).
*   **Material:** It is made of clear, transparent glass, allowing the color and opacity of the contents to be easily seen.
*   **Location:** The bottle is centered in each image, standing upright.

**Contents: Juice**
*   **Amount:** The bottle is filled almost to the base of the neck, leaving a small air gap at the top. This indicates it contains a substantial amount of liquid relative to its total volume.
*   **Color & Variety (as shown in different images):**
    *   **Orange/Peach Type:** A pale, somewhat opaque, light yellowish-orange or creamy pale yellow liquid.
    *   **Cherry Type:** A translucent, medium-to-dark reddish-brown or deep, muted red liquid.
    *   **Banana Type:** An opaque, creamy off-white or very pale, milky yellow liquid.

**Labels:**
There are two distinct labels affixed to the front surface of the bottle's main body.
*   **General Label Characteristics:**
    *   **Amount:** Two labels per bottle.
    *   **Color:** Both labels have a light beige or parchment-like background color, with a subtle gradient effect making the edges appear slightly darker or "toasted."
    *   **Border:** Each label is outlined with a thin black border.
    *   **Material:** They appear to be paper labels.

*   **Main Label (Upper):**
    *   **Location:** Positioned centrally on the upper half of the bottle's main rectangular body.
    *   **Shape & Proportions:** It is roughly square with slightly rounded corners. Its width is a significant portion of the bottle's width, perhaps around 70-80%.
    *   **Content:** This label features a simple, stylized color illustration of a fruit, which changes depending on the juice type:
        *   A single orange sphere with a small green leaf.
        *   Two red cherries joined by a green stem.
        *   A bunch of three yellow bananas.
        The fruit illustration is centrally located within this label.

*   **Secondary Label (Lower):**
    *   **Location:** Positioned centrally on the lower half of the bottle's main body, below the main label and closer to the base.
    *   **Shape & Proportions:** This label is rectangular, noticeably wider than it is tall. Its width is similar to the main label, but its height is significantly less, perhaps about one-third to one-half the height of the main label.
    *   **Content:** It displays the text "100% Juice" in a black, clear, slightly rounded sans-serif or simple serif font. The text is centered and fills most of the label's width.

**Overall Impression:**
The product presents a simple, somewhat artisanal or rustic aesthetic due to the label design and the classic small bottle form. The clear glass and distinct juice colors, along with the fruit illustrations, effectively communicate the product's nature and flavor variety. The proportions suggest a single-serving beverage.
""",

    "pushpins": """
Okay, here's a detailed description of the product based on the provided images:

**Overall Product:**
The images depict a collection of yellow thumbtacks neatly organized within a clear, rectangular plastic storage container. The container and its contents are presented against a stark black background, which makes the clear plastic and the bright yellow tacks highly visible.

**The Storage Container:**

*   **Size and Proportions (Container):**
    *   The container is rectangular, visibly longer than it is wide.
    *   It is divided into a grid of 15 individual, equally-sized square compartments, arranged in 3 rows and 5 columns.
    *   The overall length of the container is equivalent to the width of five compartments, and its width is equivalent to the height of three compartments.
    *   The depth of the container appears relatively shallow, sufficient to hold the thumbtacks without them protruding significantly when the lid is closed (though the lid is shown open or as the top surface).
    *   A small, slightly protruding tab or clasp is visible at the center of one of the longer edges, indicating a hinged lid mechanism. The hinge itself runs along the opposite long edge.
*   **Color (Container):** The container, including its internal dividers, is made of a clear, translucent plastic, allowing the contents of each compartment to be easily seen.
*   **Amount (Container):** There is one such storage container shown. It contains 15 individual compartments.

**The Thumbtacks (Push Pins):**

*   **Amount (Thumbtacks):** There are exactly 15 thumbtacks, with one thumbtack placed in each of the 15 compartments of the container.
*   **Color (Thumbtacks):**
    *   The heads of the thumbtacks are a solid, bright, matte yellow color, possibly a marigold or goldenrod yellow.
    *   The pins are a standard metallic silver-grey.
*   **Size and Proportions (Thumbtacks):**
    *   Each thumbtack consists of two main parts: a flat, circular head and a sharp, slender metal pin.
    *   The diameter of the yellow head appears to be roughly two-thirds to three-quarters the length of the metal pin.
    *   The head itself has a noticeable thickness, though it's significantly less than its diameter, giving it a disc-like appearance.
    *   The metal pin is straight and tapers to a sharp point.
    *   The overall length of a thumbtack is the combined length of its pin and the thickness of its head.
*   **Length (Thumbtacks):**
    *   The pin portion is the longest single dimension of the thumbtack.
    *   If a compartment's side is considered 'X' units, the pin's length is approximately 0.6 to 0.7X, and the head's diameter is about 0.4 to 0.5X. The total length of a thumbtack, when laid flat, would be slightly less than the width of a single compartment.
*   **Location (Thumbtacks):**
    *   Each thumbtack is located individually within one of the 15 compartments.
    *   Their orientation within each compartment is varied and appears random across the images: some are lying on their side with the pin horizontal, some are point-up, some are point-down, and others are angled. This suggests they are loosely placed rather than fixed.

In summary, the product is a set of 15 bright yellow-headed, silver-pinned thumbtacks, each individually housed in one of the 15 square compartments of a clear, rectangular plastic organizer case. The case is designed for small item storage and allows for easy visibility of its contents.
""",

    "screw_bag": """
Okay, here's a detailed description of the product based on the provided images, focusing on the requested attributes:

**Overall Product:**
The product is a small hardware kit, consisting of bolts, nuts, and washers, packaged together in a clear, resealable plastic bag. The items are metallic and appear to be made of steel or a similar silver-colored metal alloy.

**Packaging:**
*   **Type & Size:** The items are contained within a small, transparent, rectangular plastic bag. The bag appears to be a standard "grip seal" or "ziplock" style, with a press-to-close mechanism along its top edge.
*   **Location:** The hardware components are located loosely inside this bag. Their arrangement varies across the images, indicating they are not fixed in place.
*   **Color:** The bag itself is clear/transparent. Along the resealable edge, there is a printed band, predominantly white. This band features repeating recycling symbols (triangle with "04" inside and "PE-LD" underneath), indicating it's made of Low-Density Polyethylene. There are also small, white dashed lines or markings visible along the seal.
*   **Proportions:** The bag is wider than it is tall (excluding the seal area). The longest bolt, when placed diagonally, almost spans the width of the usable bag area.

**Contents - Hardware Components:**

All hardware components are **metallic silver-grey** in color, suggesting a common material like steel, possibly zinc-plated for corrosion resistance.

1.  **Bolts (Socket Head Cap Screws):**
    *   **Amount:** There are **two** bolts.
    *   **Type:** Both are socket head cap screws, recognizable by their cylindrical heads with an internal hexagonal drive (for an Allen key).
    *   **Color:** Metallic silver-grey.
    *   **Length & Proportions:**
        *   One bolt is noticeably **longer** than the other.
        *   The **longer bolt** has a threaded shaft that appears to be roughly 1.5 to 1.75 times the length of the shorter bolt's threaded shaft. Its overall length (head included) might be approximately 4-5 times its head diameter.
        *   The **shorter bolt** has an overall length perhaps 2.5-3 times its head diameter.
        *   Both bolts have identical head diameters and head heights. The threaded portion starts immediately below the head (fully threaded).
    *   **Size (relative):** The diameter of the threaded shaft of the bolts is uniform and designed to fit the nuts and washers.

2.  **Nuts:**
    *   **Amount:** There are **two** nuts.
    *   **Type:** Standard hexagonal nuts.
    *   **Color:** Metallic silver-grey.
    *   **Size & Proportions:**
        *   They are sized to match the threads of the bolts.
        *   Their thickness is approximately half their width (flat-to-flat distance across the hexagon).
        *   The outer diameter (point-to-point across the hexagon) is larger than the head diameter of the bolts.

3.  **Washers:**
    There are two distinct types of washers, two of each type:
    *   **A) Flat Washers:**
        *   **Amount:** There are **two** flat washers.
        *   **Type:** Standard circular flat washers with a central hole.
        *   **Color:** Metallic silver-grey.
        *   **Size & Proportions:**
            *   Their internal hole diameter is sized to fit over the bolt shafts.
            *   Their outer diameter is slightly larger than the outer diameter of the nuts (point-to-point).
            *   They are relatively thin compared to their diameter.
    *   **B) Split Lock Washers (Spring Washers):**
        *   **Amount:** There are **two** split lock washers.
        *   **Type:** Circular spring washers, characterized by a split and an axial twist, causing one end to be slightly raised relative to the other.
        *   **Color:** Metallic silver-grey.
        *   **Size & Proportions:**
            *   Their internal hole diameter is sized to fit over the bolt shafts.
            *   Their outer diameter is comparable to, or very slightly smaller than, the flat washers.
            *   They are thicker than the flat washers due to their spring design and have a more substantial cross-section.

**Summary of Amounts:**
*   Bolts: 2 (one long, one short)
*   Nuts: 2
*   Flat Washers: 2
*   Split Lock Washers: 2
*   Total individual hardware pieces: 8

**General Proportions:**
*   The nuts and washers are appropriately sized for the diameter of the bolts.
*   The main distinguishing feature among the bolts is their length.
*   The bag is appropriately sized to contain these components loosely.
""",

    "splicing_connectors": """
The images display sets of electrical lever-nut style wire connectors, each set consisting of two connectors linked by a short piece of insulated electrical wire. These are shown against a silver/gray metallic mesh background with a repeating diamond or rhombic pattern.

**Object (Connectors):**
*   **Size & Proportions:**
    *   The connectors are relatively small, designed for manual operation.
    *   Each connector has a roughly rectangular block shape.
    *   The images show variations in the connectors based on the number of wire ports:
        *   **Two-port connectors:** These are the most compact. Their width (across the levers) is slightly greater than their length (along the axis of the wire connection). The body appears roughly square when viewed from the side where levers are, with the translucent part extending slightly.
        *   **Three-port connectors:** These are wider than the two-port versions due to the additional lever and port, while their length (depth into which the wire inserts) and height remain similar.
        *   **Five-port connectors:** These are the widest, featuring five levers, making them significantly wider than they are long or tall.
    *   The orange levers are small, individual tabs, proportioned to be easily flipped by a fingertip.
*   **Color:**
    *   The main body of each connector is made of **translucent or clear plastic**, allowing some visibility of the internal metallic contacts.
    *   The articulating levers on each connector are a **bright, vibrant orange**.
    *   Internal contact points visible through the translucent housing appear metallic **silver/gray**.
*   **Amount:**
    *   Each assembly consistently features **two** connectors, one at each end of the connecting wire.
    *   The number of levers (and thus wire ports) per connector varies: images show connectors with **two, three, or five** orange levers. Both connectors in a single assembly always have the same number of levers.

**Object (Connecting Wire):**
*   **Size & Length:**
    *   The wire is **short**. Its length is consistently several times longer than the length of an individual connector body. If a connector body is approximately 1 unit in length, the wire is about 3-4 units long.
    *   Using the background mesh as a very rough scale, the wire spans approximately 7-8 of the diamond-shaped openings in the mesh.
*   **Color:**
    *   The insulation of the wire appears in three distinct colors across the different images:
        *   **Bright yellow**
        *   **Vibrant red**
        *   **Medium blue**
    *   Faint black text (e.g., "20AWG," "200°C") is visible on some of the yellow and red wires, indicating specifications.
*   **Amount:**
    *   There is **one** piece of wire connecting the two connectors in each assembly.

**Overall Assembly:**
*   **Location:** All assemblies are positioned **horizontally and centered** on the metallic mesh background.
*   **Proportions:**
    *   The wire is the dominant component in terms of length for the entire assembly.
    *   The overall width of the assembly is dictated by the width of the connectors (which varies with the number of ports), while its length is primarily the wire plus the short length of the two connectors.
    *   The assembly is symmetrical, with identical connectors at each end of the wire.

**Background:**
*   The background is a **silver/gray metallic mesh** with a uniform, repeating diamond or rhombic pattern. The voids within the mesh appear **dark or black**, providing contrast.
""",

    "bottle": """
Okay, based on the images provided, here's a general description of the object:

**General Description:**
The images show a consistent top-down view of a circular opening, characteristic of the mouth of a bottle or a similar cylindrical container.

*   **Size:**
    *   The opening itself is circular and appears to be of a moderate diameter, typical for a beverage bottle or similar container.
    *   The rim or neck of the container surrounding the opening has a noticeable thickness, composed of several concentric layers or contours visible from this angle.
    *   The absolute size cannot be determined without a reference scale.

*   **Location:**
    *   The object is centrally located within each image frame.
    *   The opening is positioned at the top of what is presumably a neck structure, leading down into the body of the container.

*   **Color:**
    *   The primary color of the container material is very dark, appearing as a dark brown, deep amber, or almost black.
    *   There are subtle reflections on the inner surfaces of the neck, catching the light and revealing an amber or orange-brown hue, particularly noticeable in some images (e.g., the third one). This suggests the material might be translucent dark glass.
    *   The interior visible through the opening is extremely dark, appearing black, indicating either significant depth, an opaque dark lining, or that it's filled with a very dark substance.

*   **Length (Interpreted as Depth/Diameter):**
    *   The "length" in terms of the diameter of the opening is consistent across the images.
    *   The visible "length" or depth into the neck shows several concentric rings before descending into darkness. The full length/height of the container is not visible.

*   **Amount:**
    *   There is **one** such object (the opening of a container) depicted in each image.
    *   The amount of content within the container is not clearly visible; the interior is simply dark. It could be empty and shadowed, or filled with a very dark liquid.
""",

    "cable": """
This product is a multi-conductor electrical cable, shown in cross-section across several images.

1.  **Object's Size:**
    *   The overall diameter of the cable appears to be moderately small, likely in the range of a few millimeters to perhaps 1-2 centimeters.
    *   Each of the three inner conductors is roughly a third of the inner diameter of the main cable, also appearing to be a few millimeters in diameter.
    *   The individual copper strands making up the core of each conductor are very fine.

2.  **Location:**
    *   The images show a cross-sectional view, looking at the end of a cut cable.
    *   Three insulated conductors are located centrally within a larger, circular outer sheath or jacket.
    *   These three conductors are arranged in a roughly triangular or trefoil formation, nestled together to fill the inner space of the outer jacket.

3.  **Color:**
    *   **Outer Sheath:** A light color, appearing off-white, very light gray, or pale blue-gray depending on the image lighting. It has a slightly textured or matte finish.
    *   **Inner Insulated Conductors:**
        *   One conductor has **yellow-green** insulation (often indicative of an earth/ground wire).
        *   One conductor has **blue** insulation (often indicative of a neutral or phase wire).
        *   One conductor has **brown** insulation (often indicative of a phase wire).
    *   **Conductive Core:** The metallic strands within each insulated conductor are a shiny **copper** color.

4.  **Length:**
    *   The images only show a cross-section, so the actual length of the cable is not visible. Cables like this are typically manufactured in long, continuous lengths and sold by the meter/foot or on spools.

5.  **Amount:**
    *   There is **one** main outer cable assembly.
    *   Inside, there are **three** individually insulated inner conductors.
    *   Each of these three conductors is composed of **multiple** (many) fine strands of copper wire. Counting them precisely is difficult from the images, but each core appears to contain approximately 15-30+ individual strands, indicating a stranded wire construction (for flexibility) rather than a solid core.
""",

    "capsule": """
Okay, based on the images provided:

**General Description of the Product:**

The images display a single, elongated pharmaceutical-style capsule.

*   **Size & Length:** The capsule is of a typical size for oral medication, being significantly longer than it is wide. Without a scale, its exact dimensions cannot be determined, but it appears to be a standard-sized capsule. Its length is divided into two sections.
*   **Location:** The capsule is centrally located in each image, positioned horizontally against a plain, light-colored (likely white or off-white) background.
*   **Color:** The capsule is bi-colored. One end (approximately a little less than half its length, on the left in the orientation shown) is a solid, glossy black. The other, slightly longer section is a matte orangey-brown or terracotta color. The number "500" is printed in white or a very light color on this orangey-brown portion.
*   **Amount:** There is one (1) such capsule visible in each image. All images depict the same single object.
""",

    "carpet": """
This image displays a close-up, macro view of a woven textile fabric.

*   **Object:** The product is a piece of woven fabric.
*   **Size:** The image shows a small section, likely a swatch, of the fabric. The individual threads appear to be of a medium thickness, and the weave itself is relatively tight but with discernible individual strands, suggesting a somewhat coarse or textured feel rather than a very fine, smooth fabric. The overall size of the product this fabric would be used for (e.g., upholstery, garment) cannot be determined from this close-up.
*   **Location:** The fabric pattern fills the entire frame of the image. Based on the texture and color, this type of fabric is often used for upholstery, home furnishings (like cushions or curtains), or heavy-duty accessories.
*   **Color:** The fabric is predominantly grey, with a heathered or variegated appearance. It's composed of interwoven threads in multiple shades of grey, including lighter (almost off-white or silver) and darker (charcoal or slate grey) tones, and potentially some with a slightly brownish or taupe undertone, giving it a neutral, textured look.
*   **Length:** In the image, we see short, repeating segments of threads as they are interwoven. The overall length of the actual fabric piece or bolt cannot be determined from this close-up.
*   **Amount:** The image shows a dense weave with a high amount of threads packed closely together, both horizontally (weft) and vertically (warp), to create a solid, textured surface. The total amount of fabric available is not depicted.
""",

    "grid": """
Based on the images, here's a general description of the product:

*   **Object Type:** The product is a type of metallic mesh or grating, likely expanded metal mesh due to the characteristic diamond/elongated hexagonal pattern.
*   **Size:**
    *   **Overall Product Size:** Indeterminate from these close-up images. It's a material that likely comes in sheets or rolls.
    *   **Feature Size:** The individual strands of the mesh appear relatively thin, and the openings (the diamond/hexagonal voids) seem to be of a small to medium size relative to each other. Without a scale reference, absolute dimensions cannot be given.
*   **Location:** The images show the mesh placed against a flat, lighter-colored, slightly textured background. There is no context for its intended application or environmental location. It appears to be photographed in isolation, possibly as a product sample.
*   **Color:** The mesh is depicted in shades of gray, suggesting a metallic material (e.g., steel, aluminum, or a similar alloy). It's a darker gray compared to the lighter gray background. The images are in grayscale, so the true color isn't visible, but it presents as a standard metallic gray.
*   **Length:** The *depicted section* fills the frame of each image. The actual length of the product (if it's a sheet or roll) is unknown from these close-ups.
*   **Amount:** The images show a single, continuous piece or section of this mesh material. There are many repeating units (the diamond/hexagonal openings) visible within the frame.

**In summary:** The images display a close-up of a dark gray, metallic mesh with a repeating pattern of small to medium-sized, diamond-shaped or elongated hexagonal openings. The material is shown against a lighter gray background, and its overall dimensions and specific application are not discernible from these views.
""",

    "hazelnut": """
Based on the images, here's a general description of the product:

*   **Object:** The product is a single hazelnut (also known as a filbert) in its shell.
*   **Size:** It appears to be a typical, relatively small size characteristic of a hazelnut. While no specific measurements can be given without a scale, it's a bite-sized nut.
*   **Location:** In each of the four images, the hazelnut is centrally positioned against a consistent, plain, very dark (appearing black or dark grey) background.
*   **Color:** The shell is predominantly a warm, light to medium reddish-brown. It features subtle, darker, fine vertical striations running along its length. The base of the nut, where it was once attached to the husk, presents a contrasting, rougher-textured, paler brown or tan area. Some views show a slightly darker tip.
*   **Length & Shape:** The hazelnut exhibits an ovoid or slightly conical shape, generally being somewhat elongated. It is broader at its base and tapers gently towards the opposite end, which can appear slightly pointed or more rounded depending on the viewing angle.
*   **Amount:** Each of the four images displays one (1) hazelnut. The series of images provides different perspectives of this single item.
""",

    "leather": """
Okay, based on the image provided:

This appears to be a close-up, detailed view of a single piece of material.

*   **Object/Material Type:** The image shows a textured surface, strongly resembling leather or a high-quality faux leather/vinyl. It has a characteristic grain pattern with irregular, somewhat polygonal indentations.
*   **Size:** The absolute size of the overall object or the piece of material shown cannot be determined from this close-up. The texture elements (the "grains") appear relatively small, suggesting this is a magnified view of a larger surface or a sample swatch.
*   **Location:** The material fills the entire frame of the image. There is no background or contextual information to determine its broader location or what product it is part of.
*   **Color:** The material is a consistent, uniform shade of rich, medium to dark brown. There are subtle variations in shading due to the texture and lighting, but the base color is distinctly brown.
*   **Length:** Similar to size, the actual length of this piece of material (or the product it's on) is indeterminate from this close-up view. We are only seeing a section of it.
*   **Amount:** The image displays a single, continuous surface of this one type of material.

**General Description:**
The image showcases a detailed, close-up view of a single piece of rich brown, textured material, likely leather or a synthetic equivalent. It features a consistent, irregular grain pattern across its surface. Due to the close-up nature, the overall size, length, and specific location or application of this material cannot be determined from the image alone, but it presents as a uniform sample or section of a larger item.
""",

    "metal_nut": """
Okay, here's a general description of the product based on the visual information from the images:

**General Description:**

The images display a **single unit** (Amount) of a small, metallic component.

*   **Location:** The object is centrally positioned against a dark, uniform, and featureless background in all provided images.
*   **Color:** The object has a metallic, silvery-grey color. There are variations in tone, with some areas appearing brighter due to light reflection, suggesting a somewhat matte or brushed, rather than highly polished, surface. Subtle greenish or bluish undertones might be present, potentially due to the lighting or the material's composition.
*   **Shape & Size/Length:**
    *   The object has a symmetrical, four-lobed or cross-like shape. It features a prominent central circular hole, which appears to be surrounded by a slightly raised collar or flange.
    *   Four equally spaced, curved arms or lobes extend outwards from this central hub. The ends of these arms are rounded.
    *   Without any scale reference, the exact **size** cannot be determined. However, judging by the level of detail visible (e.g., surface texture, slight machining marks), it appears to be a relatively small component, likely measurable in centimeters or a few inches.
    *   Its "overall **length**" would best be described as its diameter if measured from the tip of one arm to the tip of the opposing arm. It also possesses a discernible thickness, though this is less apparent from the top-down perspective shown.
*   **Surface:** The surface appears somewhat textured or mottled, not perfectly smooth, with some concentric circular patterns visible on the central flat areas between the hole and the arms.
""",

    "pill": """
Okay, here's a general description of the product based on the images and the requested attributes:

The images display a single, small, oval-shaped tablet.

*   **Size & Length:** The tablet appears to be of a standard size for an oral pill, though exact dimensions cannot be determined from the images alone. Its oval shape means it is longer along one axis than the other.
*   **Location:** The tablet is centrally located within each image, set against a dark, uniform (likely black) background. On the surface of the tablet itself, the characters "FF" are debossed (imprinted) into the center.
*   **Color:** The primary color of the tablet is off-white or a very light cream. It is flecked with numerous small, irregularly shaped speckles of a reddish-brown or maroon color.
*   **Amount:** There is one (1) tablet depicted in the images. The reddish-brown speckles are present in a sparse to moderate amount, distributed across the visible surface.
""",

    "screw": """
This product is a single metal screw, depicted in multiple grayscale images.

*   **Amount:** One screw is shown in each image.
*   **Location (in image):** The screw is consistently the central focus, placed against a plain, light-toned (off-white or light gray) background. It is generally oriented horizontally or slightly angled.
*   **Color:** It appears metallic gray, typical for steel or treated metal fasteners (as seen in the grayscale representation).
*   **Size and Length (Visual Assessment):**
    *   The screw appears to be of a common, medium length, suitable for general fastening applications (e.g., woodworking or light construction).
    *   It features a countersunk head, which is wider than the shank and tapers to allow the screw to sit flush with or below the surface of the material it's driven into. The head has a star-shaped drive recess (e.g., Torx).
    *   The cylindrical shank has coarse, widely-spaced threads covering approximately the lower half to two-thirds of its total length. The remaining portion of the shank directly below the head is smooth and unthreaded.
    *   The tip is sharply pointed to aid in starting the screw into material.
""",

    "tile": """
Okay, based on the images, here's a general description of the product (which appears to be a surface finish or material):

The images depict a close-up view of a surface characterized by a dense, speckled pattern.

*   **Color:** The background is a light, slightly desaturated gray, possibly with a very subtle cool (bluish or greenish) undertone. Upon this base, there are numerous darker speckles, appearing as a medium to dark charcoal gray.
*   **Object's Size (Speckles):** The speckles vary significantly in size. There are many small, dot-like particles, as well as larger, more irregular blotches which appear to be clusters or aggregations of smaller elements.
*   **Location:** The speckles are distributed across the entire visible surface in a relatively even, though somewhat random, manner. There are no large, clear areas; the pattern is consistent throughout.
*   **Length:** The "length" of these speckles varies. The smallest are near-circular (short length and width). The larger, irregular blotches are more elongated in various orientations, with some forming meandering or amorphous shapes of greater length than width.
*   **Amount:** There is a high amount or density of these darker speckles, covering a substantial portion of the light gray background, creating a visually busy and textured appearance.
""",

    "toothbrush": """
This is a close-up image of the head of a toothbrush.

*   **Object:** Toothbrush head.
*   **Size:** The head appears to be of a compact to standard adult size, with an elongated oval shape. The bristles are relatively short.
*   **Location:** The bristles are densely packed onto the white plastic base of the toothbrush head. A small portion of the white neck/handle is visible at the bottom.
*   **Color:**
    *   **Bristles:** The bristles are bi-colored, featuring distinct red and white tufts.
    *   **Head Base:** The plastic of the head itself is white.
*   **Length:** The bristles appear to be of a uniform, relatively short length across all tufts. The head itself is longer than it is wide.
*   **Amount:**
    *   There are approximately 36 individual bristle tufts visible.
    *   These tufts are arranged in 4 columns running along the length of the head, and approximately 9 rows across its width.
    *   The color pattern of the tufts is alternating: the two outer columns feature an alternating sequence of white and red tufts (e.g., W-R-W-R...), while the two inner columns feature the opposite alternating sequence (e.g., R-W-R-W...). This results in 18 red tufts and 18 white tufts.
""",

    "transistor": """
Based on the images, here's a general description of the product:

*   **Product:** A small electronic component, likely a transistor or a similar three-leaded device in a TO-92 style package.
*   **Amount:** There is **one** such component prominently featured in each image.
*   **Location:** The component is mounted on a copper-clad perforated prototyping board (often called a perfboard or veroboard). Its leads are inserted through the holes of this board.
*   **Color:**
    *   The main body of the component is **black** (likely plastic or epoxy).
    *   The leads (legs) are **silvery metallic**.
    *   The prototyping board has **copper-orange** conductive tracks and dark (appearing black) circular holes.
    *   There is a faint, light-colored (white or grey) marking on the flat face of the component body, which appears to be a letter ('T' or 'G') within a circle, varying slightly between images or due to lighting.
*   **Size (Relative):**
    *   The component is **small**. Its body is wider than the spacing between two adjacent holes on the perfboard, spanning approximately three to four hole spacings in width.
    *   The body is relatively compact, with its height and width being similar, and its depth (front to back) being less.
*   **Length (Leads):**
    *   The component has **three short** metallic leads. These leads extend from the bottom of the black body, are bent outwards, and then downwards to pass through the perfboard holes. The visible length of the leads before they enter the board is short, comparable to the height of the component's body.
""",

    "wood": """
Based on the images, this product appears to be samples of wood or a wood-like veneer, likely for surfacing applications.

*   **Size:** The images are close-up shots, so the overall size of the final product (e.g., a plank or sheet) cannot be determined. However, the grain patterns shown range from fine and relatively tight lines to broader, more open figuring. The "medullary rays" or flecks visible in some samples (especially the first one, typical of quarter-sawn oak) are small, indicating a fine texture.
*   **Location:** The images show the surface of the material itself, not its installed location. However, this type of material is commonly used for interior applications such as flooring, wall paneling, furniture, cabinetry, or decorative surfaces.
*   **Color:** The product exhibits a range of natural wood tones.
    *   Image 1: Light to medium brown with a slightly warm, golden or reddish undertone, and distinct darker brown grain lines/flecks.
    *   Image 2: Medium, slightly warmer brown, with more consistent vertical graining.
    *   Image 3: A richer, reddish-brown hue with a more pronounced, slightly wavy vertical grain.
    *   Image 4: Lighter tan/brown base with prominent darker brown, almost black, vertical streaks and figuring.
*   **Length:** The grain patterns are shown running vertically across the full height of each image sample. This suggests that if these are planks or panels, the grain would extend along their primary length. The actual length of the product units is not discernible from these close-ups.
*   **Amount:** The images display four distinct samples or variations of the product, each showcasing a different wood grain pattern and coloration. The total quantity of product available is not indicated.

In summary, the images depict four variations of a wood or wood-veneer product, characterized by vertical grain patterns of varying fineness and figuring, in a palette of light tan, golden brown, medium brown, and reddish-brown tones, with some samples featuring prominent darker streaks.
""",

    "zipper": """
This product is a close-up view of a continuous coil zipper.

*   **Size:** The images provide a detailed view, but the overall length and exact gauge (width of teeth/tape) cannot be definitively determined without a scale reference. However, it appears to be a medium-sized zipper, with the teeth being relatively fine and closely spaced, and the tape having a noticeable width on either side.
*   **Location:** The zipper is shown isolated against a plain white background. The coil teeth are centrally located along the length of the supporting fabric tape.
*   **Color:** The entire product, including both the plastic coil teeth and the woven fabric tape, is a uniform dark gray or black color. The tape has a matte, textured appearance.
*   **Length:** The images show a segment of the zipper; the full length is not depicted. Such zippers are typically sold in various lengths.
*   **Amount:** The images display a single, continuous piece of zipper.
"""
}