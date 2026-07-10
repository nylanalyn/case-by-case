# Artwork Brief

All game art belongs under `static/images/` so Django can serve it directly.
Create the listed directories as needed. Use the exact filenames below.

## Shared Direction

The town should feel rain-soaked, old, coastal, and isolated without identifying
an actual country, state, or region. It is grounded and lived-in, not gothic,
post-apocalyptic, or overtly supernatural. Use overcast daylight, wet surfaces,
muted evergreen, weathered red, gray-blue, and sodium-warm window light.

Do not include readable text, logos, flags, license plates, maps, or famous
landmarks. Leave visual room around doors, counters, paths, and people so the
game can place UI near the image later.

## Location Images

Format for every location image: `1600x1067`, PNG, 3:2 landscape. These should
be clear establishing shots, not abstract mood images.

### Town Square

- File: `static/images/locations/town-square.png`
- Prompt: "A readable establishing shot of a small, rain-soaked town square in
  an unknown coastal region. Wet brick pavement, a dry fountain, an old clock
  on a pole, modest town hall windows, benches, noticeboards, and a few dark
  evergreen trees. Overcast afternoon, restrained gray-blue and evergreen
  palette, warm light in a few windows. Grounded contemporary mystery game
  environment, no people in close view, no readable text, no flags, 3:2."

### Diner

- File: `static/images/locations/diner.png`
- Prompt: "A small independent diner on a rainy main street in an unknown
  coastal town. Large front windows, fogged glass, modest neon-like glow with
  no readable words, wet pavement, a couple of stools visible inside, a coffee
  pot and counter suggested through the window. Familiar and slightly worn,
  not retro kitsch, not a chain restaurant. Overcast daylight, 3:2 landscape,
  no people in close view, no readable text."

### Library

- File: `static/images/locations/library.png`
- Prompt: "Exterior and entrance of a small town library during steady rain.
  Stone or painted wood facade, broad front steps, rain-darkened handrails,
  warm interior lamps, tall windows with shelves faintly visible. Quiet,
  practical, well used, and slightly outdated. Unknown location, grounded
  contemporary mystery game scene, 3:2 landscape, no readable text or flags."

### Sheriff's Office

- File: `static/images/locations/sheriffs-office.png`
- Prompt: "A compact local sheriff's office on a wet side street in a small
  isolated town. Plain municipal facade, one parked older patrol vehicle with
  no markings or readable plate, rain puddles, a dim office window and a
  filing cabinet silhouette inside. Competent but underfunded, not a dramatic
  police station. Unknown location, overcast daylight, 3:2 landscape, no
  readable text, badges, flags, or logos."

### Cemetery

- File: `static/images/locations/cemetery.png`
- Prompt: "A small old cemetery in persistent rain. A wet iron north gate,
  modest headstones, mossy paths, low stone walls, clipped grass, dark trees,
  and a distant bus-shelter shape beyond the grounds. Grounded local mystery,
  quiet rather than horror, overcast daylight, 3:2 landscape, no readable
  inscriptions or supernatural effects."

### River Walk

- File: `static/images/locations/river-walk.png`
- Prompt: "A narrow town river walk on a rainy gray day. Slow dark water,
  damp wooden railings, bottle caps and leaves near the edge, low brick
  buildings behind the path, distant hill and observatory dome barely visible.
  Real and inspectable details, restrained coastal small-town atmosphere,
  3:2 landscape, no people in close view, no readable text."

### Bus Depot

- File: `static/images/locations/bus-depot.png`
- Prompt: "A humble regional bus depot in a small rain-soaked town. Covered
  platform, a handwritten-looking schedule board with no legible text, wet
  concrete, empty benches, one aging bus in the far background, fluorescent
  interior light. Practical, lonely, and ordinary, not a major transit hub.
  Unknown location, 3:2 landscape, no readable words or logos."

### Observatory

- File: `static/images/locations/observatory.png`
- Prompt: "A small hilltop public observatory above a rainy isolated town.
  Compact white dome, weathered service building, damp gravel path, dark pine
  trees, broad view toward the river and town lights below. Closed more often
  than open, but still real and cared for. Overcast blue-gray daylight, 3:2
  landscape, no science-fiction elements, no readable signage."

## Core NPC Portraits

Format: `1024x1024` PNG, portrait crop from chest up, transparent background.
Keep the camera height, scale, diffuse rainy-day lighting, and painterly-real
style consistent across all five. Do not include text or props that obscure the
face. These are reserved for `static/images/npcs/`.

- `static/images/npcs/mara-bell.png`: Mara Bell, diner worker in her late 30s
  or 40s, practical dark work shirt, tired observant eyes, hair pinned back,
  expression suggests she remembers every regular's order and every lie.
- `static/images/npcs/halden-price.png`: Deputy Halden Price, careful local
  deputy in a worn rain jacket over a plain uniform shirt, cracked notebook in
  hand but not blocking the face, reserved and attentive.
- `static/images/npcs/iris-vale.png`: Iris Vale, librarian, layered cardigan
  and practical glasses, dry intelligent expression, a little ink or dust on
  her fingers, not whimsical or stereotypically magical.
- `static/images/npcs/nico-saye.png`: Nico Saye, bus depot clerk, weatherproof
  jacket, alert but sleep-deprived, looks like someone who has watched too many
  late buses arrive wrong.
- `static/images/npcs/june-arlet.png`: June Arlet, cemetery caretaker, rain
  shell or work jacket, garden gloves tucked away, calm expression that refuses
  to discuss the north gate.

## Brindle Creek Residents

These ten people are permanent, named residents rather than paper-doll
combinations. They wander between locations over the course of a day, so each
portrait needs to be immediately recognizable at a glance. Use the same
`1024x1024` transparent PNG, chest-up crop, camera height, diffuse rainy-day
lighting, and painterly-real style as the core NPC portraits. Do not include
text, logos, or a background; the game places them over the current location.

- `static/images/npcs/beverly-kett.png`: Beverly Kett, retired postal clerk in
  her early 60s, practical raincoat, short silver hair, knowing expression,
  small canvas shoulder bag; looks like she has noticed who came and went.
- `static/images/npcs/colin-voss.png`: Colin Voss, dock repairer in his late
  40s, weathered work jacket, dark curly hair going gray at the temples, calm
  face, faint machine-oil smudge on one cuff.
- `static/images/npcs/darlene-mott.png`: Darlene Mott, school bus driver in
  her 50s, bright-but-worn waterproof jacket, cropped hair, alert practical
  expression; warm but not sugary.
- `static/images/npcs/elliot-ward.png`: Elliot Ward, night-shift stocker in
  his late 20s, hooded overshirt over work clothes, tired eyes, close-cropped
  hair, carrying no visible store branding.
- `static/images/npcs/frances-pell.png`: Frances Pell, florist in her 40s,
  soft rain shell, loose dark braid, composed expression, a hint of green on
  her fingers; no bouquet obscuring the face.
- `static/images/npcs/gabriel-shaw.png`: Gabriel Shaw, appliance repairer in
  his late 30s, layered work shirt and rain jacket, neatly trimmed beard,
  friendly but preoccupied expression.
- `static/images/npcs/helen-rook.png`: Helen Rook, former science teacher in
  her late 60s, weatherproof coat, patterned scarf, white curly hair, bright
  observant eyes; practical rather than eccentric.
- `static/images/npcs/jasper-quill.png`: Jasper Quill, handyman in his 30s,
  faded utility jacket, tousled hair, paint on one cuff, wry half-smile.
- `static/images/npcs/lila-barnes.png`: Lila Barnes, bakery assistant in her
  early 20s, oversized cardigan beneath a raincoat, dark hair in a loose bun,
  sleepy but kind expression; no chef costume.
- `static/images/npcs/martin-crowe.png`: Martin Crowe, volunteer firekeeper
  in his 50s, plain dark field jacket, close-shaved head, steady expression,
  modest flashlight clipped at his side but not blocking the face.

They should read as ordinary locals with real routines: not glamorous, not
costumed, and not posed as suspects. Their distinction should come from face,
silhouette, age, and everyday outerwear rather than dramatic props.
