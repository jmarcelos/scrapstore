#primeira classe

mongo 'ds059682.mongolab.com:59682/scrapstore' -u scrapstore -p scrapstore --eval "printjson(db.HOMELIST_COLLETION.find({$or: [ {'url' : {$regex : '.*/celulares-e-telefones/.*'}},{'url' : {$regex : '.*/Eletronicos/.*'}},{'url' : {$regex : '.*/tv-e-home-theater/.*'}},{'url' : {$regex : '.*/informatica/.*'}},{'url' : {$regex : '.*/celulares-e-telefonia-fixa/.*'}},{'url' : {$regex : '.*/tablets/.*'}},{'url' : {$regex : '.*/TelefoneseCelulares/.*'}},]}).forEach(function(doc){doc.priority = 1;db.HOMELIST_COLLETION.save(doc);}));"
mongo 'ds059682.mongolab.com:59682/scrapstore' -u scrapstore -p scrapstore --eval "db.HOMELIST_COLLETION.find({$or: [ {'url' : {$regex : '.*/eletrodomesticos/.*'}},{'url' : {$regex : '.*/games/.*'}},{'url' : {$regex : '.*/musica/.*'}},{'url' : {$regex : '.*/brinquedos/.*'}},{'url' : {$regex : '.*/CineFoto/.*'}},{'url' : {$regex : '.*/Eletroportateis/.*'}},{'url' : {$regex : '.*/Games/.*'}},{'url' : {$regex : '.*/filmesemusicas/.*'}},]}).forEach(function(doc){doc.priority = 5;db.HOMELIST_COLLETION.save(doc);});"
mongo 'ds059682.mongolab.com:59682/scrapstore' -u scrapstore -p scrapstore --eval "db.HOMELIST_COLLETION.find().forEach(function(doc){doc.last_scan_date = new Date('25-09-2015');db.HOMELIST_COLLETION.save(doc)});"

db.HOMELIST_COLLETION.find({$or: [ {'url' : {$regex : '.*/celulares-e-telefones/.*'}},
      {'url' : {$regex : '.*/Eletronicos/.*'}},
      {'url' : {$regex : '.*/tv-e-home-theater/.*'}},
      {'url' : {$regex : '.*/informatica/.*'}},
      {'url' : {$regex : '.*/celulares-e-telefonia-fixa/.*'}},
      {'url' : {$regex : '.*/tablets/.*'}},
      {'url' : {$regex : '.*/TelefoneseCelulares/.*'}},
      {'url' : {$regex : '.*/eletrodomesticos/.*'}},
      {'url' : {$regex : '.*/games/.*'}},
      {'url' : {$regex : '.*/musica/.*'}},
      {'url' : {$regex : '.*/brinquedos/.*'}},
      {'url' : {$regex : '.*/CineFoto/.*'}},
      {'url' : {$regex : '.*/Eletroportateis/.*'}},
      {'url' : {$regex : '.*/Games/.*'}},
      {'url' : {$regex : '.*/filmesemusicas/.*'}},
     ]}).forEach(
function(doc){
    doc.priority = 1;
    db.HOMELIST_COLLETION.save(doc);
});
--
-- # segunda classe
db.HOMELIST_COLLETION.find({$or: [ {'url' : {$regex : '.*/eletrodomesticos/.*'}},
      {'url' : {$regex : '.*/games/.*'}},
      {'url' : {$regex : '.*/musica/.*'}},
      {'url' : {$regex : '.*/brinquedos/.*'}},
      {'url' : {$regex : '.*/CineFoto/.*'}},
      {'url' : {$regex : '.*/Eletroportateis/.*'}},
      {'url' : {$regex : '.*/Games/.*'}},
      {'url' : {$regex : '.*/filmesemusicas/.*'}},
     ]}
).forEach(
function(doc){
    doc.priority = 5;
    db.HOMELIST_COLLETION.save(doc);
});
-- db.HOMELIST_COLLETION.find().forEach(function(doc){doc.last_scan_date = new ISODate('25-09-2015');db.HOMELIST_COLLETION.save(doc)});
