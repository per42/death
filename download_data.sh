#! /usr/bin/env sh

mkdir -p data

curl https://www.scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/tabell-och-diagram/preliminar-statistik-over-doda/ -o data/prel.xlsx -L
curl http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/BefUtvKon1749 -H "Content-Type: application/json" -d @scb_queries/BefUtvKon1749.json | json_pp --json_opt utf8,pretty > data/BefUtvKon1749.json
curl http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101G/ManadBefStatRegion -H "Content-Type: application/json" -d @scb_queries/ManadBefStatRegion.json | json_pp --json_opt utf8,pretty > data/ManadBefStatRegion.json
