
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'PCDATA OPENTAGOPEN CLOSETAGOPEN HEADEROPEN HEADERCLOSE TAGATTRNAME TAGCLOSE LONETAGCLOSE ATTRASSIGN ATTRVALUE1OPEN ATTRVALUE1STRING ATTRVALUE1CLOSE ATTRVALUE2OPEN ATTRVALUE2STRING ATTRVALUE2CLOSEheader : HEADEROPEN TAGATTRNAME attributes HEADERCLOSE root\n\troot : element\n\t\t\t| element PCDATA\n\troot : PCDATA element\n\t\t\t| PCDATA element PCDATA\n\telement : opentag children closetag\n\t\t\t   | lonetag\n\topentag : OPENTAGOPEN TAGATTRNAME attributes TAGCLOSE\n\tclosetag : CLOSETAGOPEN TAGATTRNAME TAGCLOSE\n\tlonetag : OPENTAGOPEN TAGATTRNAME attributes LONETAGCLOSE\n\tattributes : attribute attributes\n\t\t\t\t  | empty\n\tattribute : TAGATTRNAME ATTRASSIGN attrvalue\n\tattrvalue : ATTRVALUE1OPEN ATTRVALUE1STRING ATTRVALUE1CLOSE\n\t\t\t\t | ATTRVALUE2OPEN ATTRVALUE2STRING ATTRVALUE2CLOSE\n\tchildren : child children\n\t\t\t\t| empty\n\tchild : elementchild : PCDATAempty :'
    
_lr_action_items = {'ATTRVALUE1STRING':([12,],[20,]),'TAGATTRNAME':([1,3,5,11,16,24,30,31,35,],[3,4,4,-13,24,4,-14,-15,39,]),'ATTRASSIGN':([4,],[8,]),'PCDATA':([10,15,17,19,22,25,26,27,36,37,38,40,],[14,23,-7,25,32,-19,-18,25,-6,-10,-8,-9,]),'ATTRVALUE2CLOSE':([21,],[31,]),'CLOSETAGOPEN':([17,19,25,26,27,28,29,34,36,37,38,40,],[-7,-20,-19,-18,-20,35,-17,-16,-6,-10,-8,-9,]),'HEADEROPEN':([0,],[1,]),'HEADERCLOSE':([3,5,6,7,9,11,30,31,],[-20,-20,10,-12,-11,-13,-14,-15,]),'ATTRVALUE1CLOSE':([20,],[30,]),'OPENTAGOPEN':([10,14,17,19,25,26,27,36,37,38,40,],[16,16,-7,16,-19,-18,16,-6,-10,-8,-9,]),'LONETAGCLOSE':([5,7,9,11,24,30,31,33,],[-20,-12,-11,-13,-20,-14,-15,37,]),'TAGCLOSE':([5,7,9,11,24,30,31,33,39,],[-20,-12,-11,-13,-20,-14,-15,38,40,]),'ATTRVALUE1OPEN':([8,],[12,]),'ATTRVALUE2OPEN':([8,],[13,]),'ATTRVALUE2STRING':([13,],[21,]),'$end':([2,15,17,18,22,23,32,36,37,40,],[0,-2,-7,-1,-4,-3,-5,-6,-10,-9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'attribute':([3,5,24,],[5,5,5,]),'child':([19,27,],[27,27,]),'closetag':([28,],[36,]),'lonetag':([10,14,19,27,],[17,17,17,17,]),'header':([0,],[2,]),'attrvalue':([8,],[11,]),'attributes':([3,5,24,],[6,9,33,]),'element':([10,14,19,27,],[15,22,26,26,]),'root':([10,],[18,]),'children':([19,27,],[28,34,]),'empty':([3,5,19,24,27,],[7,7,29,7,29,]),'opentag':([10,14,19,27,],[19,19,19,19,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> header","S'",1,None,None,None),
  ('header -> HEADEROPEN TAGATTRNAME attributes HEADERCLOSE root','header',5,'p_header_root','xtm_parser.py',195),
  ('root -> element','root',1,'p_root_element','xtm_parser.py',203),
  ('root -> element PCDATA','root',2,'p_root_element','xtm_parser.py',204),
  ('root -> PCDATA element','root',2,'p_root_pcdata_element','xtm_parser.py',212),
  ('root -> PCDATA element PCDATA','root',3,'p_root_pcdata_element','xtm_parser.py',213),
  ('element -> opentag children closetag','element',3,'p_element','xtm_parser.py',221),
  ('element -> lonetag','element',1,'p_element','xtm_parser.py',222),
  ('opentag -> OPENTAGOPEN TAGATTRNAME attributes TAGCLOSE','opentag',4,'p_opentag','xtm_parser.py',234),
  ('closetag -> CLOSETAGOPEN TAGATTRNAME TAGCLOSE','closetag',3,'p_closetag','xtm_parser.py',243),
  ('lonetag -> OPENTAGOPEN TAGATTRNAME attributes LONETAGCLOSE','lonetag',4,'p_lonetag','xtm_parser.py',253),
  ('attributes -> attribute attributes','attributes',2,'p_attributes','xtm_parser.py',262),
  ('attributes -> empty','attributes',1,'p_attributes','xtm_parser.py',263),
  ('attribute -> TAGATTRNAME ATTRASSIGN attrvalue','attribute',3,'p_attribute','xtm_parser.py',278),
  ('attrvalue -> ATTRVALUE1OPEN ATTRVALUE1STRING ATTRVALUE1CLOSE','attrvalue',3,'p_attrvalue','xtm_parser.py',286),
  ('attrvalue -> ATTRVALUE2OPEN ATTRVALUE2STRING ATTRVALUE2CLOSE','attrvalue',3,'p_attrvalue','xtm_parser.py',287),
  ('children -> child children','children',2,'p_children','xtm_parser.py',299),
  ('children -> empty','children',1,'p_children','xtm_parser.py',300),
  ('child -> element','child',1,'p_child_element','xtm_parser.py',316),
  ('child -> PCDATA','child',1,'p_child_pcdata','xtm_parser.py',323),
  ('empty -> <empty>','empty',0,'p_empty','xtm_parser.py',331),
]
