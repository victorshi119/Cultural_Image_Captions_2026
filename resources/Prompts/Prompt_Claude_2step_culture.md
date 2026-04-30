I'm participating in americasnlp challenge where we take an image then generate a caption in target langauge (in our case guarani). I'm thinking about feeding this culture knowledge along with the image so that langauge model knows about guarani culture (hopefully). can you help me articulate my prompt to my speicalized LLM to look into this file and then search the internet what we should add into this that are culture relevant to guarani? I want you to give me the best prompt possible for this, and here is the github repo for the comeptition: https://github.com/AmericasNLP/americasnlp2026#important-dates, and we are competing on the Guarani track only.

4:01 PM
Claude responded: I've read your culture file and the competition page.

Architected specialized LLM prompt for culturally-grounded Guarani image captioning enhancement
Architected specialized LLM prompt for culturally-grounded Guarani image captioning enhancement
I've read your culture file and the competition page. Your file is already solid — it covers cosmovision, food, drinks, mythology, crafts, music, etc. The key insight for designing this prompt: since this is image captioning (not general cultural QA), every addition should be visually grounded — things that can actually appear in a photograph. Your file's Section 14 ("Señales Visuales Clave") is exactly right, and the prompt should push the research LLM to think the same way.

I'll build the prompt as a markdown file so you can save it and iterate.


Created a file, ran a command, read a file
Created a file, ran a command, read a file
A few notes on the design choices, in case you want to tweak:

Why four phases instead of one open-ended ask. A single "go research Guaraní culture" prompt tends to produce a Wikipedia-flavored essay. Forcing audit → gap analysis → drafting → deliverables makes the LLM commit to what's missing before it writes, which gives you something more useful to merge into your file.

Why the visual-grounding constraint is repeated. The biggest failure mode for this kind of knowledge file is that it accumulates beautiful philosophical content (cosmovision, teko porã, etc.) that doesn't help a model decide whether a photo shows a chipa vendor or a generic bakery. The prompt pushes hard against that.

Why an anti-stereotype list. If you only feed positive cultural cues, the model will start projecting them onto every image — captioning a city street as if it were a rural festival. Telling the LLM to surface what is not distinctly Guaraní is just as valuable as telling it what is.

Why the linguistic-style section (gap #11). Your file teaches the model what Guaraní culture contains but not how Guaraní speakers describe images. ChrF++ rewards surface n-gram overlap, so getting the style right (sentence structure, verb forms, whether Jopara is okay) probably affects your score more than any single cultural fact.

Two things you may want to adjust before sending:

If your "specialized LLM" has a strict context window, you may want to ask for Phase 1 + Phase 2 first, then Phase 3 + Phase 4 in a follow-up turn.
Double-check the deadline section in the README — the milestones list 2025 dates but the repo title is 2026, which is suspicious. Worth confirming with the organizers before you commit a workflow timeline.

Guarani research prompt
Document · MD 

Claude finished the response
You said: Follow the instruction of the pasted text and reference the .

# Prompt: Expand Guaraní Cultural Knowledge Base for Image Captioning ## Role You are a research assistant with deep expertise in **Paraguayan and Guaraní culture, the Guaraní language (avañe'ẽ), and visual ethnography**. You also understand how vision-language models use cultural priors to generat

pasted


guarani_culture_knowledge.txt
175 lines

txt

Follow the instruction of the pasted text and reference the .txt file as instructed

4:03 PM
Claude responded: I'll work through this systematically.

Strategized systematic audit and research expansion of cultural knowledge file
Strategized systematic audit and research expansion of cultural knowledge file
I'll work through this systematically. Let me start with Phase 1 (audit) using the file already in context, then move into web research for Phase 2.

PHASE 1 — Audit of the existing file
§	Section	Strengths	Weaknesses	Verdict
1	Lengua y cosmovisión	Names avañe'ẽ and Jopara correctly	Not visually grounded; abstract	Revise — keep only as preface
2	Cosmovisión / creencias	Mentions tekoha, teko porã	Pure philosophy, zero pixels	Cut to one line
3	Organización social	—	Generic "hospitality / community"; could describe any culture	Cut
4	Alimentación	Names chipa, sopa paraguaya, mbeju, vori vori	Missing: chipa guasu, mbaipy, puchero, asado, locro, kosereva, dulce de mamón, reviro; no visual descriptors (color/shape/size)	Revise + expand
5	Bebidas	Tereré ritual described	Missing mate cocido, caña, mosto, clericó; no mention of yuyos (medicinal herbs) crushed in mortar with tereré	Revise
6	Pohã ñana	Concept named	Names zero plants. A captioning model needs kohü, ka'a he'ẽ, cedrón Paraguay, menta'i, koku etc.	Revise (major)
7	Flora / fauna	—	No species names in Guaraní; "loros, etc." is useless	Revise (major)
8	Mercados	Names Mercado 4	Missing Mercado de Abasto, Mercado Central de Luque, ferias, yuyera (herb seller archetype)	Revise
9	Artesanía	Ñandutí, ao po'i	Missing: filigree silver, encaje ju, poyvi, karanda'y weaving, ceramics of Itá/Areguá, hammocks, tallado en madera, cuero crudo	Revise (major)
10	Música y danza	Arpa, polka, guarania, danza de la botella	Missing: purahéi jahe'o, galopa, conjunto típico instruments (guitarra, requinto), banda koygua	Revise
11	Historia	—	Not visually grounded	Cut
12	Religión	Sincretism named	Missing: Virgen de Caacupé, capillas rurales, fiestas patronales, altars, processions	Revise (major)
13	Cultura rural	Hammock, mandioca	Missing: rancho, tatakua, corral, carro de bueyes, fogón, pozo	Revise (major)
14	Señales visuales	Useful list	Too short; needs every section to have its own	Revise
15	Directrices	Decent	Should add anti-stereotype list	Revise
16	Leyendas	Detailed	Mostly NOT visually grounded — leyendas appear in art, not photos. Risk: model over-attributing forest scenes to Pombero	Revise (cut redundancy + add visual disclaimer)
Cross-cutting weaknesses

The file calls everything "Guaraní" without distinguishing Paraguayan mestizo culture (criollo/koygua) from Indigenous Guaraní peoples (Mbyá, Aché, Pãi Tavyterã, Avá, Guaraní Ñandeva). This is a major fidelity risk.
Almost no Guaraní vocabulary for visible objects.
No section on dress, architecture, festivals, children's games, sports, or occupations.
No guidance on Guaraní caption style (verb forms, sentence structure).
Now Phase 2 — let me search authoritative sources.


Assembled comprehensive Paraguayan cultural documentation with organized deliverables
Assembled comprehensive Paraguayan cultural documentation with organized deliverables
I have enough to produce all four deliverables. Phase 1 was completed above; here are Phases 2, 3, and 4.

PHASE 2 — Gap analysis with proposed additions
#	Gap	Proposed additions	Key sources
1	Vestimenta — file mentions ñandutí + ao po'i but not the actual outfit. No regional/festival distinction.	Section on traje típico (typói + pollera con volantes + encaje ju + dos trenzas + rosario tupãsy; hombre: camisa ao po'i + pantalón oscuro + faja + pañuelo + sombrero piri + poncho para'i de 60 listas). Distinguish festival/folkloric from daily wear (mostly absent in everyday photos).	EcuRed, Trenalsur, sofiaschmodarte blog, Ministerio de Cultura
2	Arquitectura/vivienda — completely absent.	Section on kuláta jovái (planta simétrica con koty guasu central y dos culatas), ógaguy / korredor jere (galería), paredes de estaqueo + barro o adobe, techo de paja kapi'í sobre cumbrera, tatakua, pozo de balde. Casas urbanas de Asunción coloniales + ruinas jesuíticas (arenisca roja).	Wikipedia "Culata Yobái", ARQA, revista Mandu'a, Plan de Gestión Misiones
3	Festividades visibles — ninguna mencionada.	Sección dedicada a San Juan Ára (juegos del fuego), Caacupé 8 dic, Semana Santa con chipa y tatakua, fiestas patronales con bandas koygua.	mec.gov.py, ABC Color, Última Hora, Wikipedia "Virgen de Caacupé"
4	Juegos infantiles — ausentes.	Sección con pandorga, trompo, valita, tikichuela, kambuchi jejoka, payana, gallito ciego, tuka'ẽ.	ABC Color "Juegos de siempre", Portal Guarani, Correo Paraguayo
5	Utensilios/objetos domésticos — solo "hamaca" mencionada vagamente.	Sección con angu'a (mortero), tatakua, kyha (hamaca), guampa (de cuerno o madera), bombilla, ajaka (canasto), termo, cocina a leña, fogón, machete, carro de bueyes.	Wikipedia "Tatakua", Alacarta, EFE/Swissinfo
6	Vocabulario guaraní visual — el archivo no da glosario.	Glosario completo: árboles (tajy, yvyra pytã, samu'û, karanda'y, mbokaja…), frutas (arasa, mburukuja, ñangapiry, pakuri…), animales (jagua, mbarakaja, ryguasu, vaka, kavaju, jakare, mbói, panambi…), colores y materiales.	Portal Guarani (Guasch), Idioma-Guarani blog, Tesoro de Montoya
7	Distinción Mbya / Pãi / Aché / Avá / paraguayo mestizo — el archivo lo agrupa todo.	Sección sobre 19 pueblos indígenas, cinco familias lingüísticas; señales visuales que distinguen Mbya (jeguaka, opy/óga guasu, mbaraka, takua) de criollo paraguayo (typói folclórico). Aclarar que "guaraní" en imágenes paraguayas suele referir a paraguayos no-indígenas.	IWGIA, Wikipedia "Pueblos indígenas de Paraguay", Tierraviva, INE 2022
8	Deportes y ocio — no existe.	Sección con fútbol (Olimpia, Cerro, Libertad, Guaraní, Albirroja), asado/parrilla, pesca en río Paraguay/Paraná, cacería en el Chaco.	ABC Color deportes
9	Cuadros ocupacionales visuales — faltan.	Sección: chipera con ajaka en cabeza + apyteha'o, yuyera del Mercado 4, vendedor de mbeju, arenero con carro, olero/ceramista (Itá, Areguá, Tobatí), agricultor con machete, lavandera, motoquero.	Alacarta, ABC Color "La ruta de las chiperas", El Nacional, Museo del Mundo
10	Color/material/textura en guaraní — ausente.	Glosario con morotĩ (blanco), pytã (rojo), hovy (azul/verde), sa'yju (amarillo), hũ (negro), etc.; texturas: po'i (fino), guasu (grande), mirĩ (pequeño), karẽ (torcido).	Paraguayología, gramatica avañe'ẽ
11	Estilo lingüístico de captions — el archivo es solo prosa española.	Sección con 8 ejemplos pareados español↔guaraní: características (estructura SOV/SVO flexible, hetá uso de oĩ/oĩva 'hay/que está', mba'e como conector, sufijo -kuéra para plural, prenasalización mb/nd/ng). Mencionar que jopara aparece en captions periodísticos pero el track requiere guaraní.	ABC Remiandu, Wikipedia "Guarani language", Ñemitỹrã
12	Anti-estereotipos — no hay sección.	Lista explícita: maíz no es solo Paraguay, hamaca no es solo Paraguay, sombreros de paja generales no son ao po'i, mate caliente ≠ tereré frío, asado ≠ específicamente paraguayo, "indígena" en una foto no implica "guaraní", flora subtropical es compartida.	Razonamiento sintético + Wikipedia comparativo
PHASE 3 — Drafted new sections (en español, listo para pegar en el archivo)
A continuación, las secciones nuevas. Mantengo numeración 17 en adelante para insertarlas después de "Leyendas y Tradición Oral" del archivo original; varias secciones existentes deberían además ser revisadas según el audit.

17. Vestimenta tradicional y cotidiana

La gran mayoría de las imágenes paraguayas mostrarán ropa moderna común (jeans, remera, camiseta de fútbol). El traje típico solo aparece en festivales, danza folklórica, escuelas el 14 de mayo o eventos religiosos.

Traje folklórico femenino:

Typói (blusa de ao po'i, algodón blanco fino): escote amplio redondo bordado en negro, rojo o color, mangas tres cuartos rematadas con encaje ju (encaje de bolillos); un hombro a veces cae descubierto.
Pollera larga hasta los tobillos, amplia, con uno o dos volados fruncidos; suele ser blanca, color sólido o estampada.
Mantilla de ñandutí atada en un hombro y cruzada al costado.
Peinado: dos trenzas largas con moño en las puntas, adornadas con flores frescas (jazmín, rosa).
Joyas: rosario de filigrana (tupãsy), peinetas, aretes de oro, collares de coral.
Traje folklórico masculino:

Camisa de ao po'i blanca con bordados a tono en pecho, puños y cuello.
Pantalón recto oscuro (negro habitual).
Faja de seda o lana negra con flecos, o trenzada de algodón multicolor.
Pañuelo blanco o negro anudado al cuello en triángulo.
Sombrero piri (de paja, cinta negra); poncho para'i de 60 listas sobre el hombro.
Frecuentemente descalzo o con zapato negro simple.
Vestimenta indígena Mbya/Avá/Pãi (cuando aparezca):

Tipoy (vestido recto sin mangas, hasta las rodillas) en algodón o tela industrial; en fiestas se usa con bordados sencillos.
Jeguaka (corona/diadema ritual de plumas) en hombres en ceremonias, no a diario.
Mbaraka (maraca de calabaza) y takua (bastón rítmico de bambú golpeado por mujeres) en danzas religiosas.
Pintura corporal con urucú (rojo de Bixa orellana) en ceremonias.
En la vida diaria, ropa industrial común; el folclore mediático suele exagerar lo "tradicional".
Señales visuales:

Bordados blancos sobre fondo blanco → ao po'i.
Encaje circular policromo en abanicos radiales → ñandutí.
Hombre con poncho a rayas finas y sombrero de paja → traje típico paraguayo, no necesariamente gaucho.
Mujer con botellas en la cabeza bailando → galopera (no traje cotidiano).
18. Arquitectura y vivienda

Vivienda rural mestiza tradicional:

Kuláta jovái ("culatas enfrentadas"): planta simétrica con un espacio central abierto (koty guasu) y dos cuartos a los costados. Es el prototipo del rancho paraguayo.
Ógaguy / korredor / korredor jere (galería frontal, lateral o períptera): alero ancho que rodea la casa, con horcones de madera; espacio social principal donde se cuelga la kyha (hamaca), se ceba tereré y reciben visitas.
Paredes de estaqueo (palos verticales rellenos de barro) o adobe revocado; en versiones más pobres, takuára (bambú) y bosta + arcilla.
Techo de paja kapi'í quinchada sobre cumbrera de madera, dos aguas; en casas más modernas, tejas o chapa de zinc.
Piso de tierra apisonada o ladrillo.
Detrás: tatakua (horno), pozo, gallinero, plantación de mandi'o.
Vivienda urbana:

Asunción centro: casas coloniales bajas, fachada continua a la vereda, ventanas con rejas de hierro forjado, patio interior con galería; pintadas de blanco, ocre o pastel.
Barrios populares: casas de ladrillo a la vista, techo de chapa, frente con portón corredizo de hierro.
Edificios modernos en torres en la zona financiera (Asunción centro, Villa Morra, Las Mercedes).
Misiones Jesuíticas (Trinidad, Jesús, San Cosme, Santa María de Fe):

Ruinas en piedra arenisca roja, sillares; estilo barroco hispano-guaraní.
Plaza mayor cuadrada con iglesia mayor, casas de indios alineadas, talleres, cementerio.
Frisos labrados con ángeles músicos, motivos vegetales locales (yvyra pytã, mbokaja).
Tono dominante: rojizo de la arenisca contra el verde del bosque atlántico.
Señales visuales:

Techo de paja en capas + galería con horcones → rancho paraguayo, no rancho gaucho argentino (este último suele tener mojinetes y blanqueado).
Bóveda baja de ladrillos visibles con boca de un metro → tatakua.
Pared roja-anaranjada con motivos labrados, sin techo → ruina jesuítica, no edificio activo.
19. Tatakua y otros utensilios domésticos visibles

Tatakua ("agujero de fuego"): horno abovedado de barro y ladrillo en forma de cúpula, con boca de unos 60–80 cm; suele estar en el patio sobre una base de piedra o ladrillo. Usado para chipa, sopa paraguaya, mbeju, chipa guasu, asado.
Angu'a (mortero): tronco ahuecado de madera dura, con mano larga; aún se usa para machacar maíz, mandioca o yuyos. En el tereré, el angu'a pequeño machaca pohã ñana.
Kyha (hamaca paraguaya) de algodón o ñandutí, colgada en la galería; muy ancha, sin flecos como la mexicana.
Guampa: vaso para tereré, originalmente de cuerno vacuno, hoy también de madera, palo santo, acero forrado en cuero, o porongo.
Bombilla: caña metálica con filtro, para sorber tereré/mate.
Termo: cilíndrico, de plástico o acero, decorado con cuero repujado o estampados (banderas, equipos de fútbol). Casi siempre acompaña a la guampa.
Ajaka: canasto trenzado de tacuara o karanda'y, plano y ancho, usado por chiperas para cargar la mercadería en la cabeza, cubierto con un paño de ao po'i.
Apyteha'o: rodete de tela enrollada que se coloca entre la cabeza y el ajaka.
Cocina a leña: fogón con tres piedras o trípode de hierro; pava de aluminio ennegrecida.
Carro de bueyes (carreta) con ruedas de madera maciza, aún visible en zonas rurales del Chaco e interior.
20. Festividades y eventos religiosos visibles

San Juan Ára (24 de junio y todo junio) — fiesta del fuego, sincretismo hispano-guaraní:

Tatápe jehasa / tatapýi ári jehasa (caminar sobre brasas): alfombra de carbones encendidos de 3–5 m, gente descalza caminando.
Pelota tata (pelota encendida): pelota de trapo empapada en kerosene, ardiendo, pateada entre la concurrencia.
Toro candil: armazón de madera y trapos en forma de toro con cuernos en llamas; un hombre lo lleva mientras "embiste".
Yvyra sỹi (palo enjabonado): poste vertical engrasado, premio en la punta.
Kambuchi jejoka: cántaro colgado, lleno de premios, roto a palos con ojos vendados.
Paila jeheréi: lamer una sartén con monedas pegadas con caramelo.
Judas kái: muñeco de trapo relleno de petardos, colgado y quemado.
Casamiento koygua: boda paródica.
Pruebera: adivinadora con cartas.
Comidas típicas: chipa, mbeju, pajagua mascada (croqueta de mandioca y carne), pastel mandi'o, chicharõ trenzado, sopa paraguaya, batiburrillo, kosereva (dulce de naranja agria), mbaipy he'ẽ (polenta dulce de maíz).
Caacupé (8 de diciembre):

Peregrinación masiva a la Basílica de Caacupé (cúpula azul); muchos peregrinos caminan desde Asunción (54 km) durante toda la noche del 7 al 8.
Imagen de la Virgen de los Milagros / Virgen Azul: pequeña talla en madera, manto azul con flores de mburukuja (pasiflora), parada sobre globo terráqueo azul con tres estrellas doradas y la cinta tricolor paraguaya, a sus pies serpiente. En procesiones se usan andas de plata.
Vigilia con galoperas (mujeres equilibrando botellas en la cabeza).
Gigantesca aglomeración con velas, banderas paraguayas y pancartas devocionales.
Semana Santa:

Encendido masivo de tatakuas para hornear chipa.
Procesiones con cruces (kurusu).
Sopa paraguaya, chipa, chipa guasu en las mesas.
Fiestas patronales locales: bandas koygua (charanga rural), procesión del santo, fuegos artificiales, comida abundante.

Carnaval Encarnaceno (Encarnación): comparsas con plumas y trajes brillantes, similar a Río pero menor escala — no exclusivamente "guaraní", es importación brasileña.

Señales visuales:

Brasas extendidas + gente descalza saltando → tatápe jehasa, no parrillada.
Cúpula azul con domo blanco + multitud → Basílica de Caacupé.
Mujer con varias botellas equilibradas en la cabeza → galopera.
21. Juegos tradicionales infantiles y pasatiempos

Pandorga (barrilete/cometa): estructura de palillos de takuarilla, papel de colores con flecos y cola de tela; volada en patios o calles de tierra en días de viento, principalmente en agosto.
Trompo: peonza de madera dura (guayabo, arasa, sapirangy) con púa de clavo; se enrolla con piolín, se lanza, gira en el suelo. Variantes: trompo sele, trompo kora.
Valita / balita (bolitas): bolitas de cristal, acero o coco; juego de varones, en hoyo o kora'i (círculo trazado en la tierra).
Tikichuela / pisa-pizuela: rayuela; cuadrículas trazadas en tiza o palito sobre tierra.
Kambuchi jejoka: piñata de barro con premios, rota con los ojos vendados (común en San Juan).
Gallito ciego: vendado, atrapar a otros.
Tuka'ẽ: rayuela con piedra.
Pasará-pasará: ronda con cantos.
Piki pyta: variante de escondite-corrida.
Solterona, Un, do, tre, miro, karrera vosa (carrera de bolsas).
Señales visuales:

Cometa de papel hexagonal con cola larga → pandorga (más casera y simple que un kite deportivo).
Niños sentados en círculo en la tierra con bolitas → valita.
22. Glosario visual guaraní (objetos, plantas, animales, colores)

Para uso del modelo: cuando reconozca estos elementos, prefiera el sustantivo guaraní apropiado.

Plantas y árboles:

Tajy / lapacho — árbol emblemático, flores rosadas, amarillas o blancas en racimos en agosto (sin hojas).
Yvyra pytã — flores amarillas vistosas en primavera.
Samu'û — palo borracho, tronco abultado verde-grisáceo con espinas.
Karanda'y — palmera con hojas en forma de abanico.
Mbokaja — coco/cocotero (Acrocomia aculeata), tronco con espinas, fruto pequeño anaranjado.
Pindo / jata'i — palmeras de coquito.
Ygary — cedro, sagrado para los Mbya.
Urunde'y, kurupa'y, timbo, guajayvi — árboles madereros.
Yerba mate — Ilex paraguariensis; arbusto perenne, hojas duras verde oscuro.
Frutas:

Arasa — guayaba.
Aratiku — chirimoya.
Mburukuja — fruto de pasionaria; flor nacional del Paraguay.
Ñangapiry — pitanga, frutito rojo acanalado.
Pakuri, guavira, yvapurû, yvapovô, jakarati'a — frutos silvestres.
Mamón — papaya.
Mandi'o / mandioca — raíz alargada marrón con interior blanco; alimento básico.
Avati — maíz; avatiky = choclo tierno.
Animales:

Jagua — perro; jaguarete — jaguar; mbarakaja — gato.
Ryguasu — gallina; ryguasu mé — gallo.
Vaka / mymba — vaca/ganado; kavaju — caballo; kure — cerdo.
Mbói — serpiente.
Jakare — yacaré.
Panambi — mariposa.
Pykasu — paloma; mainumby — colibrí; tuka — tucán; guyra — pájaro genérico.
Karumbe — tortuga.
Tatu — armadillo.
Kapi'yvâ — carpincho.
Ñandu — ñandú; también arácnido tejedor → de ahí ñandutí.
Colores y propiedades visuales:

Morotĩ — blanco; pytã — rojo; hũ — negro; sa'yju — amarillo; hovy — azul/verde; kara'ã — gris.
Guasu — grande; mirĩ / 'i — pequeño; po'i — fino, delgado; piru — flaco/seco; karẽ — torcido; vera — brillante.
Objetos cotidianos:

Óga — casa; óga guasu — casa grande, también templo Mbya.
Kyha — hamaca; apyka — banco/silla.
Ao — ropa, tela; ao po'i — tela fina.
Kambuchi — cántaro de barro.
Yrenda / kambuchi y'a — cántaro de agua.
Mbaraka — maraca/guitarra (genérico para instrumento de cuerda).
Ajaka — canasto.
Tata — fuego; tatakua — horno; tanimbu — ceniza.
23. Distinciones étnicas y regionales (importante para no confundir)

Paraguay tiene 19 pueblos indígenas en cinco familias lingüísticas. La familia guaraní incluye seis pueblos: Aché, Avá Guaraní, Mbya, Pãi Tavyterã, Guaraní Ñandeva y Guaraní Occidental. Pero:

La mayoría de la población paraguaya no es indígena: es mestiza ("criolla", a veces autodenominada koygua) y habla guaraní paraguayo, no guaraní mbya.
La cultura folklórica paraguaya (chipa, ñandutí, polka, traje típico, San Juan) es mestiza, no indígena.
Lo "indígena guaraní" propiamente dicho (Mbya, Pãi) tiene marcadores visuales distintos: comunidades en zonas selváticas, opy (templo) de palmas, mbaraka+takua en ceremonias, vestimenta más sencilla en lo cotidiano.
Señales visuales que ayudan a distinguir:

Tipoy plano de algodón crudo + collares de semillas + entorno de selva → indígena (Mbya, Avá).
Typói bordado + pollera de volantes + escenario folklórico → paraguayo mestizo en traje folklórico.
Gente común en jeans con guampa y termo en mano → paraguayo cotidiano (mestizo o no, no es identificable solo por la imagen).
⚠ Tensión señalada: el archivo original engloba todo bajo "guaraní" sin distinguir. Para el captioning, conviene preferir términos como "paraguayo/a", "campesino/a paraguayo/a", "mujer paraguaya" cuando el sujeto sea mestizo, y reservar "indígena Mbya / Avá / Pãi" cuando se vean marcadores específicos.

24. Deportes, ocio y vida moderna

Fútbol: deporte central. Equipos populares: Olimpia (negro y blanco, franja vertical), Cerro Porteño (azul y rojo), Libertad (negro y amarillo), Guaraní (rojo y blanco a rayas, "El Aborigen / El Legendario"). Selección nacional La Albirroja (camiseta a rayas blancas y rojas verticales). Estadio Defensores del Chaco. Hinchas con cornetas y bombo, banderas extensas.
Asado: parrilla con carne vacuna (costilla, vacío, chorizo); habitual los domingos. No es exclusivo del Paraguay; también argentino, uruguayo, brasileño.
Pesca en los ríos Paraguay y Paraná: pacú, dorado, surubí, mandi'í; cañas de pescar y embarcaciones pequeñas.
Tereré rupá: refrigerio matutino antes del tereré (chipa so'o, empanadas, sándwich).
Cumpleaños y reuniones: típicamente al aire libre, en galería o patio, con polka, asado, sopa paraguaya y mbeju.
Vida urbana moderna: motos en alto número (medio principal de transporte popular), shoppings, ferias de artesanía, carrera de motos.
25. Ocupaciones y figuras urbanas/rurales habituales

Chipera: mujer (a veces hombre, llamado chipero) con un ajaka lleno de chipa equilibrado en la cabeza, cubierto con un paño de ao po'i. Camina junto a rutas, en plazas, terminales y estadios. El cuello sostiene el peso; usa apyteha'o debajo. Centro de producción tradicional: Eusebio Ayala (Barrero), Coronel Bogado, Caacupé.
Yuyera: mujer (a menudo mayor) que vende manojos de hierbas medicinales frescas (pohã ñana). Se ubica en esquinas céntricas de Asunción y en el Paseo de los Yuyos del Mercado 4. Frecuentemente machaca yuyos en angu'a sobre un cajón de madera.
Olero / Ceramista: trabaja barro a mano; mujeres son la mayoría. Centros: Itá, Areguá, Tobatí. Piezas: figuras antropomorfas, jarras, ollas, pesebres, escenas de la vida campesina.
Arenero: extrae arena del río con pala y la transporta en carro tirado por caballo o burro.
Vendedor ambulante: en autopistas y semáforos; ofrece pororó (palomitas), chipa, frutas, cargadores.
Agricultor: típicamente con sombrero piri, machete, camisa de mangas largas; en cultivos de mandioca, maíz, soja, algodón, sésamo.
Lavandera: en arroyos y patios; ropa tendida en alambres.
Motoquero: repartidor en moto, muy común en Asunción.
Galopera: mujer con typói bailando con varias botellas equilibradas en la cabeza; aparece en festivales.
26. Estilo lingüístico para captions en guaraní

Características del guaraní paraguayo escrito en pies de foto o titulares:

Estructura SOV o SVO, flexible. Muchos predicados verbales sin cópula explícita.
Verbos llevan prefijo de persona pegado: o- 3ª (oguata = "camina"), a- 1ª, re- 2ª.
Plural humano con sufijo -kuéra (mitãkuéra = "los niños"), pero a menudo se omite si el contexto es claro.
Abundante oĩ / oĩva ("hay / que está") para describir presencia: Peteĩ kuña oĩ óga renondépe = "Una mujer está frente a la casa".
Nasalización marcada con tilde (ã, ẽ, ĩ, õ, ũ, ỹ); pusó ' marca oclusión glotal.
En el dialecto popular, se usa frecuentemente jopara (mezcla con español: "ahávo la escuela-pe"); el track de la competencia probablemente requiera guaraní más puro, pero registros de prensa en guaraní (ABC Remiandu) muestran préstamos hispanos comunes (kamionero, exportación).
Captions y titulares periodísticos tienden a usar oraciones cortas, voz activa, presente o pasado con sufijo -va'ekue.
Ejemplos de pares (descripción ↔ caption guaraní idiomático):

Hombre tomando tereré bajo un árbol ↔ Peteĩ karai oy'u tereré peteĩ yvyra guýpe.
Mujeres bailando la danza de la botella ↔ Kuñakuéra ojeroky botella jerokýpe. (o, más natural:) Galoperakuéra ojeroky.
Niños jugando con un trompo en la calle de tierra ↔ Mitãkuéra oñembosarái trompo reheve tape kapi'ipére.
Una chipera con su canasto sobre la cabeza ↔ Peteĩ chipera oguereko ajaka iñakã ári.
La basílica de Caacupé llena de peregrinos ↔ Caacupé tupãópe oĩ heta tapicha oguahẽva'ekue oñembo'ehag̃ua.
Lapacho en flor sobre fondo azul ↔ Tajy poty hovýre yvága.
Familia compartiendo asado en el patio ↔ Pehẽngue oñembyaty so'o kaiguépe okápe.
Mujer mayor machacando yuyos en mortero ↔ Kuña tuja oñepyrũ ojoso pohã ñana angu'ápe.
⚠ El modelo debe evitar generar Jopara con español incrustado, salvo que la competencia lo permita explícitamente.

PHASE 4 — Anti-estereotipos (lista de cuidado)
El modelo NO debe asumir lo siguiente solo porque la imagen "parece" paraguaya:

No todo paraguayo es indígena. La mayoría es mestiza. Solo describir como "indígena Mbya/Avá/Pãi" si hay marcadores claros (entorno selvático, vestimenta indígena específica, instrumentos rituales).
El maíz, la mandioca, el poroto y la calabaza son pan-latinoamericanos. No describir un plato con maíz como "típicamente guaraní" sin más contexto.
La hamaca no es exclusiva del Paraguay. Aparece en todo el trópico americano. El distintivo paraguayo es la combinación hamaca + galería + tereré.
El asado, el mate caliente y el sombrero de paja son compartidos con Argentina, Uruguay, sur de Brasil. El tereré frío con yuyos sí es un marcador fuerte de Paraguay (también NE argentino).
El traje típico solo aparece en festivales y danzas. En la vida cotidiana paraguaya, la gente viste igual que en cualquier país sudamericano: jeans, remera, camisetas de fútbol, bermudas. Imágenes urbanas modernas son la norma.
No toda mujer con canasta sobre la cabeza es chipera — puede ser frutera, vendedora de pororó, etc. La chipera específicamente lleva ajaka cubierto con paño blanco.
No toda construcción de techo de paja es paraguaya. El kuláta jovái es específico, pero un rancho de paja simple existe en todo el Cono Sur.
Los mitos (Pombero, Jasy Jateré, Karai Octubre) rara vez aparecen en fotos reales — son temas de pintura, dibujo, escultura en barro, ilustración. Si la imagen es una fotografía de paisaje, evitar atribuirla a un mito.
El ñandutí es paraguayo, pero el encaje genérico no. No describir cualquier puntilla como ñandutí sin verificar el patrón circular radial.
"Polka" en Paraguay no es la polka centroeuropea: es género propio en 6/8.
El Carnaval Encarnaceno se parece al brasileño, no es marcador étnico guaraní.
Las ruinas de piedra arenisca roja en Itapúa son jesuíticas, no aztecas, mayas, ni "ruinas guaraníes precolombinas". Son del s. XVIII.
La selva en una foto no implica automáticamente Pombero ni Jasy Jateré — describir lo visible.
Lapacho ≠ jacarandá. El lapacho (tajy) florece sin hojas en agosto en racimos densos rosa, amarillo o blanco; el jacarandá tiene flores azules-violáceas y hojas finas pinnadas.
Lista de fuentes
Fuente	URL	Confiabilidad
MEC Paraguay — Fiesta de San Juan	mec.gov.py	Alta — Ministerio de Educación y Cultura
ABC Color — Suplementos / artículos sobre tatakua, chiperas, juegos, San Juan, Caacupé	abc.com.py	Alta — diario de referencia paraguayo
Última Hora — pohã ñana, San Juan, indígenas	ultimahora.com	Alta — segundo diario nacional
Wikipedia es. — Tatacuá, Culata Yobái, Pueblos indígenas, Mbyás, Virgen de Caacupé	es.wikipedia.org	Media-alta — bien referenciada en estos artículos
Wikipedia en. — Tereré, Guaraní language, Guaraní people	en.wikipedia.org	Media-alta
IWGIA — El Mundo Indígena Paraguay	iwgia.org	Alta — organización internacional especializada
Tierraviva	tierraviva.org.py	Alta — ONG paraguaya de derechos indígenas
Asociación Indigenista del Paraguay	asociacionindigenistaparaguay.org	Alta
INE Paraguay — Censo Indígena 2022	citado vía IWGIA, AIP	Alta — fuente oficial
Portal Guarani — Antonio Guasch (flora/fauna), Roberto Vera (juegos), Rosa Brítez (cerámica), Mario Rubén Álvarez (folklore)	portalguarani.com	Alta — archivo cultural paraguayo
Idioma-Guarani blog (David Galeano Olivera)	idioma-guarani.blogspot.com	Media-alta — autor reconocido en lengua guaraní
Paraguayología	paraguayologia.com	Media — divulgación cultural seria
Ñemitỹrã (revista UNA)	revistascientificas.una.py/index.php/nemityra	Alta — revista académica de UNA
EcuRed — Traje típico de Paraguay	ecured.cu	Media — solo descriptivo, contrastado con fuentes paraguayas
Trenalsur — vestimenta	trenalsur.net	Media
ARQA, Mandu'a, ArchDaily — arquitectura	arqa.com / mandua.com.py / archdaily.com	Alta para arquitectura paraguaya contemporánea
Camino de los Jesuitas / SENATUR — Misiones	caminodelosjesuitas.com / senatur.gov.py	Alta — fuentes oficiales de turismo
UNESCO — Misiones Jesuíticas	whc.unesco.org/es/list/648	Alta
Alacarta — chipa, Sebastián Jara	alacarta.com.py	Media-alta — periodismo gastronómico paraguayo
El Nacional, OviedoPress — chiperas, San Juan	elnacional.com.py / oviedopress.com	Media
Swissinfo / Infobae / EFE — tereré, pohã ñana	swissinfo.ch / infobae.com	Alta
Pueblo Mbyá Guaraní (Brasil-PIB / ISA)	pib.socioambiental.org	Alta — Instituto Socioambiental
Tesoro de Montoya (1639) — guaranime.blogspot.com	guaranime.blogspot.com	Alta histórica — diccionario fundacional
ABC Remiandu (sección guaraní de ABC Color)	abc.com.py/especiales/remiandu	Alta — corpus de prosa periodística en guaraní
Paraguay Mba'e	paraguaymbae.com	Media — blog de viajes informado
Nota final sobre el procedimiento. Donde el archivo original ya cubría algo bien, no agregué redundancia. Donde detecté tensión (la generalización "guaraní" para toda cultura paraguaya), añadí señalamientos explícitos. Algunas categorías —en particular la moda urbana cotidiana— tienen poca documentación específicamente paraguaya en los corpus disponibles y dependen del sentido común visual; lo señalo en lugar de inventar. El glosario guaraní está conservador: los términos marcados con ortografía estándar provienen de fuentes lexicográficas verificadas (Guasch, Tesoro de Montoya, MEC). No se introdujo vocabulario fabricado.

You said: Can you make this into a .
Can you make this into a .md file?

4:11 PM
Claude responded: Done.

Determined markdown file creation approach directly
Determined markdown file creation approach directly
Done. The full document — audit, gap analysis, ten new drafted sections (17–26), anti-stereotype list, and source table — is in the markdown file above.


Guarani culture knowledge expanded
Document · MD 

Want to be notified when Claude responds?



Claude is AI and can make mistakes. Please double-check responses.
