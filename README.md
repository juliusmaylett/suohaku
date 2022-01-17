# Suohaku

Ottaa syötteeksi geojson-muodossa olevan polygon-tiedoston, joka on TM35FIN-koordinaatistossa.
Tekee haun jokaisen alueen alle jäävistä kiinteistöistä ja talleentaa ne fid-tunnisteen nimiseen XML-tiedostoon.

Haut ovat hitaita ja liian suurien alueiden kohdalla WFS-palvelin tekee aikakatkaisun. Näitä tilanteita varten kannattaa tehdä esimerkiksi Subdivide QGIS:ssä.
