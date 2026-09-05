MATCH (n) DETACH DELETE n;
CREATE (c_pinghe:Constitution {id:'c_pinghe', name:'平和质', description:'阴阳气血调和...'})
CREATE (c_qixu:Constitution {id:'c_qixu', name:'气虚质', description:'元气不足...'})
CREATE (c_yangxu:Constitution {id:'c_yangxu', name:'阳虚质', description:'阳气不足...'})
CREATE (c_yinxu:Constitution {id:'c_yinxu', name:'阴虚质', description:'阴液亏少...'})
CREATE (c_tanshi:Constitution {id:'c_tanshi', name:'痰湿质', description:'痰湿凝聚...'})
CREATE (c_shire:Constitution {id:'c_shire', name:'湿热质', description:'湿热内蕴...'})
CREATE (c_xueyu:Constitution {id:'c_xueyu', name:'血瘀质', description:'血行不畅...'})
CREATE (c_qiyu:Constitution {id:'c_qiyu', name:'气郁质', description:'气机郁滞...'})
CREATE (c_tebing:Constitution {id:'c_tebing', name:'特禀质', description:'先天失常...'})
CREATE (a_0:Acupoint {id:'acupoint_0', name:'足三里', location:'前臂 1寸', method:'热敷5分钟'})
CREATE (a_1:Acupoint {id:'acupoint_1', name:'关元', location:'头部 2寸', method:'热敷22分钟'})
CREATE (a_2:Acupoint {id:'acupoint_2', name:'气海', location:'手部 4寸', method:'刮痧15分钟'})
CREATE (a_3:Acupoint {id:'acupoint_3', name:'中脘', location:'头部 2寸', method:'指压30分钟'})
CREATE (a_4:Acupoint {id:'acupoint_4', name:'天枢', location:'足部 2寸', method:'指压13分钟'})
CREATE (a_5:Acupoint {id:'acupoint_5', name:'大椎', location:'胸部 4寸', method:'指压22分钟'})
CREATE (a_6:Acupoint {id:'acupoint_6', name:'命门', location:'前臂 1寸', method:'按揉19分钟'})
CREATE (a_7:Acupoint {id:'acupoint_7', name:'肾俞', location:'下腹部 1寸', method:'按揉5分钟'})
CREATE (a_8:Acupoint {id:'acupoint_8', name:'脾俞', location:'足部 3寸', method:'指压16分钟'})
CREATE (a_9:Acupoint {id:'acupoint_9', name:'肺俞', location:'前臂 2寸', method:'热敷16分钟'})
CREATE (a_10:Acupoint {id:'acupoint_10', name:'心俞', location:'胸部 5寸', method:'拔罐26分钟'})
CREATE (a_11:Acupoint {id:'acupoint_11', name:'肝俞', location:'手部 5寸', method:'按揉21分钟'})
CREATE (a_12:Acupoint {id:'acupoint_12', name:'胆俞', location:'上臂 1寸', method:'拔罐22分钟'})
CREATE (a_13:Acupoint {id:'acupoint_13', name:'大肠俞', location:'腰部 4寸', method:'艾灸12分钟'})
CREATE (a_14:Acupoint {id:'acupoint_14', name:'小肠俞', location:'足部 4寸', method:'拔罐23分钟'})
CREATE (a_15:Acupoint {id:'acupoint_15', name:'三阴交', location:'胸部 1寸', method:'按揉24分钟'})
CREATE (a_16:Acupoint {id:'acupoint_16', name:'阴陵泉', location:'足部 1寸', method:'拔罐8分钟'})
CREATE (a_17:Acupoint {id:'acupoint_17', name:'阳陵泉', location:'腰部 5寸', method:'指压7分钟'})
CREATE (a_18:Acupoint {id:'acupoint_18', name:'太溪', location:'足部 4寸', method:'指压22分钟'})
CREATE (a_19:Acupoint {id:'acupoint_19', name:'太冲', location:'头部 2寸', method:'拔罐26分钟'})
CREATE (a_20:Acupoint {id:'acupoint_20', name:'涌泉', location:'胸部 1寸', method:'指压10分钟'})
CREATE (a_21:Acupoint {id:'acupoint_21', name:'行间', location:'背部 5寸', method:'刮痧23分钟'})
CREATE (a_22:Acupoint {id:'acupoint_22', name:'内关', location:'前臂 4寸', method:'热敷5分钟'})
CREATE (a_23:Acupoint {id:'acupoint_23', name:'外关', location:'小腿外侧 5寸', method:'拔罐13分钟'})
CREATE (a_24:Acupoint {id:'acupoint_24', name:'合谷', location:'下腹部 3寸', method:'艾灸17分钟'})
CREATE (a_25:Acupoint {id:'acupoint_25', name:'曲池', location:'手部 1寸', method:'按揉10分钟'})
CREATE (a_26:Acupoint {id:'acupoint_26', name:'肩井', location:'手部 5寸', method:'按揉24分钟'})
CREATE (a_27:Acupoint {id:'acupoint_27', name:'风池', location:'下腹部 1寸', method:'拔罐23分钟'})
CREATE (a_28:Acupoint {id:'acupoint_28', name:'百会', location:'头部 3寸', method:'拔罐18分钟'})
CREATE (a_29:Acupoint {id:'acupoint_29', name:'神阙', location:'下腹部 4寸', method:'针刺7分钟'})
CREATE (a_30:Acupoint {id:'acupoint_30', name:'足三里2', location:'下腹部 4寸', method:'拔罐10分钟'})
CREATE (a_31:Acupoint {id:'acupoint_31', name:'关元2', location:'上臂 1寸', method:'拔罐10分钟'})
CREATE (a_32:Acupoint {id:'acupoint_32', name:'气海2', location:'手部 1寸', method:'刮痧28分钟'})
CREATE (a_33:Acupoint {id:'acupoint_33', name:'中脘2', location:'手部 1寸', method:'针刺26分钟'})
CREATE (a_34:Acupoint {id:'acupoint_34', name:'天枢2', location:'腰部 3寸', method:'热敷6分钟'})
CREATE (a_35:Acupoint {id:'acupoint_35', name:'大椎2', location:'腰部 3寸', method:'拔罐22分钟'})
CREATE (a_36:Acupoint {id:'acupoint_36', name:'命门2', location:'手部 3寸', method:'针刺8分钟'})
CREATE (a_37:Acupoint {id:'acupoint_37', name:'肾俞2', location:'前臂 3寸', method:'按揉9分钟'})
CREATE (a_38:Acupoint {id:'acupoint_38', name:'脾俞2', location:'小腿外侧 2寸', method:'刮痧27分钟'})
CREATE (a_39:Acupoint {id:'acupoint_39', name:'肺俞2', location:'头部 4寸', method:'拔罐7分钟'})
CREATE (a_40:Acupoint {id:'acupoint_40', name:'心俞2', location:'下腹部 1寸', method:'艾灸26分钟'})
CREATE (a_41:Acupoint {id:'acupoint_41', name:'肝俞2', location:'足部 1寸', method:'刮痧12分钟'})
CREATE (a_42:Acupoint {id:'acupoint_42', name:'胆俞2', location:'背部 2寸', method:'指压9分钟'})
CREATE (a_43:Acupoint {id:'acupoint_43', name:'大肠俞2', location:'足部 4寸', method:'热敷17分钟'})
CREATE (a_44:Acupoint {id:'acupoint_44', name:'小肠俞2', location:'胸部 2寸', method:'按揉12分钟'})
CREATE (a_45:Acupoint {id:'acupoint_45', name:'三阴交2', location:'前臂 3寸', method:'按揉15分钟'})
CREATE (a_46:Acupoint {id:'acupoint_46', name:'阴陵泉2', location:'足部 4寸', method:'艾灸29分钟'})
CREATE (a_47:Acupoint {id:'acupoint_47', name:'阳陵泉2', location:'足部 1寸', method:'艾灸16分钟'})
CREATE (a_48:Acupoint {id:'acupoint_48', name:'太溪2', location:'背部 1寸', method:'按揉26分钟'})
CREATE (a_49:Acupoint {id:'acupoint_49', name:'太冲2', location:'胸部 1寸', method:'指压19分钟'})
CREATE (a_50:Acupoint {id:'acupoint_50', name:'涌泉2', location:'前臂 1寸', method:'热敷30分钟'})
CREATE (a_51:Acupoint {id:'acupoint_51', name:'行间2', location:'胸部 2寸', method:'艾灸19分钟'})
CREATE (a_52:Acupoint {id:'acupoint_52', name:'内关2', location:'头部 3寸', method:'指压10分钟'})
CREATE (a_53:Acupoint {id:'acupoint_53', name:'外关2', location:'前臂 5寸', method:'拔罐8分钟'})
CREATE (a_54:Acupoint {id:'acupoint_54', name:'合谷2', location:'背部 1寸', method:'指压20分钟'})
CREATE (a_55:Acupoint {id:'acupoint_55', name:'曲池2', location:'前臂 2寸', method:'按揉9分钟'})
CREATE (a_56:Acupoint {id:'acupoint_56', name:'肩井2', location:'足部 5寸', method:'热敷16分钟'})
CREATE (a_57:Acupoint {id:'acupoint_57', name:'风池2', location:'背部 4寸', method:'热敷30分钟'})
CREATE (a_58:Acupoint {id:'acupoint_58', name:'百会2', location:'足部 1寸', method:'指压25分钟'})
CREATE (a_59:Acupoint {id:'acupoint_59', name:'神阙2', location:'胸部 3寸', method:'指压23分钟'})
CREATE (a_60:Acupoint {id:'acupoint_60', name:'足三里3', location:'前臂 2寸', method:'热敷16分钟'})
CREATE (a_61:Acupoint {id:'acupoint_61', name:'关元3', location:'小腿外侧 4寸', method:'艾灸19分钟'})
CREATE (a_62:Acupoint {id:'acupoint_62', name:'气海3', location:'背部 4寸', method:'拔罐15分钟'})
CREATE (a_63:Acupoint {id:'acupoint_63', name:'中脘3', location:'上臂 4寸', method:'按揉27分钟'})
CREATE (a_64:Acupoint {id:'acupoint_64', name:'天枢3', location:'上臂 5寸', method:'拔罐12分钟'})
CREATE (a_65:Acupoint {id:'acupoint_65', name:'大椎3', location:'上臂 3寸', method:'指压25分钟'})
CREATE (a_66:Acupoint {id:'acupoint_66', name:'命门3', location:'下腹部 1寸', method:'指压20分钟'})
CREATE (a_67:Acupoint {id:'acupoint_67', name:'肾俞3', location:'下腹部 5寸', method:'刮痧30分钟'})
CREATE (a_68:Acupoint {id:'acupoint_68', name:'脾俞3', location:'前臂 1寸', method:'热敷6分钟'})
CREATE (a_69:Acupoint {id:'acupoint_69', name:'肺俞3', location:'前臂 4寸', method:'按揉12分钟'})
CREATE (a_70:Acupoint {id:'acupoint_70', name:'心俞3', location:'小腿外侧 1寸', method:'按揉12分钟'})
CREATE (a_71:Acupoint {id:'acupoint_71', name:'肝俞3', location:'小腿外侧 2寸', method:'热敷11分钟'})
CREATE (a_72:Acupoint {id:'acupoint_72', name:'胆俞3', location:'腰部 3寸', method:'热敷16分钟'})
CREATE (a_73:Acupoint {id:'acupoint_73', name:'大肠俞3', location:'手部 3寸', method:'按揉17分钟'})
CREATE (a_74:Acupoint {id:'acupoint_74', name:'小肠俞3', location:'手部 3寸', method:'针刺11分钟'})
CREATE (a_75:Acupoint {id:'acupoint_75', name:'三阴交3', location:'头部 2寸', method:'按揉28分钟'})
CREATE (a_76:Acupoint {id:'acupoint_76', name:'阴陵泉3', location:'下腹部 2寸', method:'艾灸22分钟'})
CREATE (a_77:Acupoint {id:'acupoint_77', name:'阳陵泉3', location:'胸部 5寸', method:'指压18分钟'})
CREATE (a_78:Acupoint {id:'acupoint_78', name:'太溪3', location:'胸部 4寸', method:'艾灸23分钟'})
CREATE (a_79:Acupoint {id:'acupoint_79', name:'太冲3', location:'上臂 4寸', method:'热敷13分钟'})
CREATE (a_80:Acupoint {id:'acupoint_80', name:'涌泉3', location:'背部 2寸', method:'指压22分钟'})
CREATE (a_81:Acupoint {id:'acupoint_81', name:'行间3', location:'背部 2寸', method:'艾灸16分钟'})
CREATE (a_82:Acupoint {id:'acupoint_82', name:'内关3', location:'背部 4寸', method:'热敷18分钟'})
CREATE (a_83:Acupoint {id:'acupoint_83', name:'外关3', location:'头部 2寸', method:'按揉18分钟'})
CREATE (a_84:Acupoint {id:'acupoint_84', name:'合谷3', location:'手部 2寸', method:'针刺30分钟'})
CREATE (a_85:Acupoint {id:'acupoint_85', name:'曲池3', location:'小腿外侧 5寸', method:'拔罐24分钟'})
CREATE (a_86:Acupoint {id:'acupoint_86', name:'肩井3', location:'小腿外侧 4寸', method:'刮痧13分钟'})
CREATE (a_87:Acupoint {id:'acupoint_87', name:'风池3', location:'前臂 2寸', method:'按揉11分钟'})
CREATE (a_88:Acupoint {id:'acupoint_88', name:'百会3', location:'小腿外侧 4寸', method:'刮痧17分钟'})
CREATE (a_89:Acupoint {id:'acupoint_89', name:'神阙3', location:'小腿外侧 5寸', method:'刮痧24分钟'})
CREATE (a_90:Acupoint {id:'acupoint_90', name:'足三里4', location:'小腿外侧 5寸', method:'针刺5分钟'})
CREATE (a_91:Acupoint {id:'acupoint_91', name:'关元4', location:'足部 1寸', method:'针刺28分钟'})
CREATE (a_92:Acupoint {id:'acupoint_92', name:'气海4', location:'小腿外侧 5寸', method:'艾灸6分钟'})
CREATE (a_93:Acupoint {id:'acupoint_93', name:'中脘4', location:'背部 2寸', method:'拔罐10分钟'})
CREATE (a_94:Acupoint {id:'acupoint_94', name:'天枢4', location:'手部 3寸', method:'指压10分钟'})
CREATE (a_95:Acupoint {id:'acupoint_95', name:'大椎4', location:'上臂 1寸', method:'艾灸11分钟'})
CREATE (a_96:Acupoint {id:'acupoint_96', name:'命门4', location:'小腿外侧 2寸', method:'指压10分钟'})
CREATE (a_97:Acupoint {id:'acupoint_97', name:'肾俞4', location:'前臂 5寸', method:'按揉9分钟'})
CREATE (a_98:Acupoint {id:'acupoint_98', name:'脾俞4', location:'背部 5寸', method:'按揉18分钟'})
CREATE (a_99:Acupoint {id:'acupoint_99', name:'肺俞4', location:'前臂 2寸', method:'拔罐23分钟'})
CREATE (a_100:Acupoint {id:'acupoint_100', name:'心俞4', location:'下腹部 2寸', method:'拔罐14分钟'})
CREATE (a_101:Acupoint {id:'acupoint_101', name:'肝俞4', location:'腰部 4寸', method:'热敷28分钟'})
CREATE (a_102:Acupoint {id:'acupoint_102', name:'胆俞4', location:'小腿外侧 3寸', method:'艾灸19分钟'})
CREATE (a_103:Acupoint {id:'acupoint_103', name:'大肠俞4', location:'小腿外侧 5寸', method:'针刺25分钟'})
CREATE (a_104:Acupoint {id:'acupoint_104', name:'小肠俞4', location:'手部 3寸', method:'针刺9分钟'})
CREATE (a_105:Acupoint {id:'acupoint_105', name:'三阴交4', location:'背部 3寸', method:'针刺19分钟'})
CREATE (a_106:Acupoint {id:'acupoint_106', name:'阴陵泉4', location:'背部 2寸', method:'针刺26分钟'})
CREATE (a_107:Acupoint {id:'acupoint_107', name:'阳陵泉4', location:'腰部 2寸', method:'针刺13分钟'})
CREATE (a_108:Acupoint {id:'acupoint_108', name:'太溪4', location:'头部 2寸', method:'热敷16分钟'})
CREATE (a_109:Acupoint {id:'acupoint_109', name:'太冲4', location:'下腹部 2寸', method:'指压21分钟'})
CREATE (a_110:Acupoint {id:'acupoint_110', name:'涌泉4', location:'头部 3寸', method:'指压18分钟'})
CREATE (a_111:Acupoint {id:'acupoint_111', name:'行间4', location:'上臂 2寸', method:'针刺17分钟'})
CREATE (a_112:Acupoint {id:'acupoint_112', name:'内关4', location:'前臂 5寸', method:'拔罐26分钟'})
CREATE (a_113:Acupoint {id:'acupoint_113', name:'外关4', location:'足部 4寸', method:'刮痧12分钟'})
CREATE (a_114:Acupoint {id:'acupoint_114', name:'合谷4', location:'手部 3寸', method:'刮痧6分钟'})
CREATE (a_115:Acupoint {id:'acupoint_115', name:'曲池4', location:'头部 2寸', method:'艾灸16分钟'})
CREATE (a_116:Acupoint {id:'acupoint_116', name:'肩井4', location:'胸部 4寸', method:'艾灸19分钟'})
CREATE (a_117:Acupoint {id:'acupoint_117', name:'风池4', location:'腰部 3寸', method:'刮痧30分钟'})
CREATE (a_118:Acupoint {id:'acupoint_118', name:'百会4', location:'腰部 1寸', method:'热敷22分钟'})
CREATE (a_119:Acupoint {id:'acupoint_119', name:'神阙4', location:'腰部 3寸', method:'刮痧24分钟'})
CREATE (a_120:Acupoint {id:'acupoint_120', name:'足三里5', location:'前臂 5寸', method:'刮痧6分钟'})
CREATE (a_121:Acupoint {id:'acupoint_121', name:'关元5', location:'前臂 5寸', method:'刮痧6分钟'})
CREATE (a_122:Acupoint {id:'acupoint_122', name:'气海5', location:'足部 5寸', method:'针刺14分钟'})
CREATE (a_123:Acupoint {id:'acupoint_123', name:'中脘5', location:'前臂 3寸', method:'针刺19分钟'})
CREATE (a_124:Acupoint {id:'acupoint_124', name:'天枢5', location:'头部 2寸', method:'艾灸17分钟'})
CREATE (a_125:Acupoint {id:'acupoint_125', name:'大椎5', location:'腰部 1寸', method:'指压21分钟'})
CREATE (a_126:Acupoint {id:'acupoint_126', name:'命门5', location:'胸部 1寸', method:'针刺25分钟'})
CREATE (a_127:Acupoint {id:'acupoint_127', name:'肾俞5', location:'腰部 5寸', method:'热敷15分钟'})
CREATE (a_128:Acupoint {id:'acupoint_128', name:'脾俞5', location:'胸部 3寸', method:'热敷7分钟'})
CREATE (a_129:Acupoint {id:'acupoint_129', name:'肺俞5', location:'小腿外侧 4寸', method:'针刺19分钟'})
CREATE (a_130:Acupoint {id:'acupoint_130', name:'心俞5', location:'足部 5寸', method:'拔罐6分钟'})
CREATE (a_131:Acupoint {id:'acupoint_131', name:'肝俞5', location:'手部 1寸', method:'艾灸27分钟'})
CREATE (a_132:Acupoint {id:'acupoint_132', name:'胆俞5', location:'手部 5寸', method:'拔罐26分钟'})
CREATE (a_133:Acupoint {id:'acupoint_133', name:'大肠俞5', location:'头部 1寸', method:'艾灸18分钟'})
CREATE (a_134:Acupoint {id:'acupoint_134', name:'小肠俞5', location:'前臂 3寸', method:'艾灸16分钟'})
CREATE (a_135:Acupoint {id:'acupoint_135', name:'三阴交5', location:'小腿外侧 4寸', method:'艾灸18分钟'})
CREATE (a_136:Acupoint {id:'acupoint_136', name:'阴陵泉5', location:'前臂 4寸', method:'刮痧21分钟'})
CREATE (a_137:Acupoint {id:'acupoint_137', name:'阳陵泉5', location:'下腹部 1寸', method:'拔罐11分钟'})
CREATE (a_138:Acupoint {id:'acupoint_138', name:'太溪5', location:'手部 2寸', method:'按揉14分钟'})
CREATE (a_139:Acupoint {id:'acupoint_139', name:'太冲5', location:'前臂 5寸', method:'热敷7分钟'})
CREATE (a_140:Acupoint {id:'acupoint_140', name:'涌泉5', location:'下腹部 2寸', method:'艾灸25分钟'})
CREATE (a_141:Acupoint {id:'acupoint_141', name:'行间5', location:'腰部 1寸', method:'艾灸22分钟'})
CREATE (a_142:Acupoint {id:'acupoint_142', name:'内关5', location:'下腹部 2寸', method:'刮痧30分钟'})
CREATE (a_143:Acupoint {id:'acupoint_143', name:'外关5', location:'背部 3寸', method:'热敷24分钟'})
CREATE (a_144:Acupoint {id:'acupoint_144', name:'合谷5', location:'下腹部 2寸', method:'艾灸12分钟'})
CREATE (a_145:Acupoint {id:'acupoint_145', name:'曲池5', location:'背部 4寸', method:'针刺7分钟'})
CREATE (a_146:Acupoint {id:'acupoint_146', name:'肩井5', location:'上臂 4寸', method:'刮痧22分钟'})
CREATE (a_147:Acupoint {id:'acupoint_147', name:'风池5', location:'下腹部 1寸', method:'热敷20分钟'})
CREATE (a_148:Acupoint {id:'acupoint_148', name:'百会5', location:'头部 2寸', method:'指压14分钟'})
CREATE (a_149:Acupoint {id:'acupoint_149', name:'神阙5', location:'下腹部 3寸', method:'针刺30分钟'})
CREATE (a_150:Acupoint {id:'acupoint_150', name:'足三里6', location:'手部 5寸', method:'指压9分钟'})
CREATE (a_151:Acupoint {id:'acupoint_151', name:'关元6', location:'手部 5寸', method:'指压13分钟'})
CREATE (a_152:Acupoint {id:'acupoint_152', name:'气海6', location:'腰部 5寸', method:'拔罐17分钟'})
CREATE (a_153:Acupoint {id:'acupoint_153', name:'中脘6', location:'小腿外侧 1寸', method:'热敷18分钟'})
CREATE (a_154:Acupoint {id:'acupoint_154', name:'天枢6', location:'足部 1寸', method:'艾灸29分钟'})
CREATE (a_155:Acupoint {id:'acupoint_155', name:'大椎6', location:'胸部 1寸', method:'刮痧18分钟'})
CREATE (a_156:Acupoint {id:'acupoint_156', name:'命门6', location:'前臂 1寸', method:'刮痧24分钟'})
CREATE (a_157:Acupoint {id:'acupoint_157', name:'肾俞6', location:'手部 5寸', method:'按揉16分钟'})
CREATE (a_158:Acupoint {id:'acupoint_158', name:'脾俞6', location:'上臂 5寸', method:'指压17分钟'})
CREATE (a_159:Acupoint {id:'acupoint_159', name:'肺俞6', location:'手部 4寸', method:'指压12分钟'})
CREATE (a_160:Acupoint {id:'acupoint_160', name:'心俞6', location:'头部 2寸', method:'按揉27分钟'})
CREATE (a_161:Acupoint {id:'acupoint_161', name:'肝俞6', location:'背部 3寸', method:'按揉21分钟'})
CREATE (a_162:Acupoint {id:'acupoint_162', name:'胆俞6', location:'手部 1寸', method:'刮痧12分钟'})
CREATE (a_163:Acupoint {id:'acupoint_163', name:'大肠俞6', location:'手部 5寸', method:'拔罐23分钟'})
CREATE (a_164:Acupoint {id:'acupoint_164', name:'小肠俞6', location:'小腿外侧 4寸', method:'针刺22分钟'})
CREATE (a_165:Acupoint {id:'acupoint_165', name:'三阴交6', location:'头部 1寸', method:'按揉24分钟'})
CREATE (a_166:Acupoint {id:'acupoint_166', name:'阴陵泉6', location:'手部 4寸', method:'刮痧18分钟'})
CREATE (a_167:Acupoint {id:'acupoint_167', name:'阳陵泉6', location:'胸部 3寸', method:'拔罐5分钟'})
CREATE (a_168:Acupoint {id:'acupoint_168', name:'太溪6', location:'背部 2寸', method:'刮痧27分钟'})
CREATE (a_169:Acupoint {id:'acupoint_169', name:'太冲6', location:'足部 2寸', method:'热敷5分钟'})
CREATE (a_170:Acupoint {id:'acupoint_170', name:'涌泉6', location:'手部 5寸', method:'热敷9分钟'})
CREATE (a_171:Acupoint {id:'acupoint_171', name:'行间6', location:'上臂 4寸', method:'刮痧9分钟'})
CREATE (a_172:Acupoint {id:'acupoint_172', name:'内关6', location:'背部 3寸', method:'指压24分钟'})
CREATE (a_173:Acupoint {id:'acupoint_173', name:'外关6', location:'胸部 3寸', method:'艾灸7分钟'})
CREATE (a_174:Acupoint {id:'acupoint_174', name:'合谷6', location:'手部 3寸', method:'艾灸14分钟'})
CREATE (a_175:Acupoint {id:'acupoint_175', name:'曲池6', location:'足部 3寸', method:'热敷17分钟'})
CREATE (a_176:Acupoint {id:'acupoint_176', name:'肩井6', location:'手部 1寸', method:'针刺18分钟'})
CREATE (a_177:Acupoint {id:'acupoint_177', name:'风池6', location:'腰部 3寸', method:'刮痧8分钟'})
CREATE (a_178:Acupoint {id:'acupoint_178', name:'百会6', location:'小腿外侧 1寸', method:'按揉13分钟'})
CREATE (a_179:Acupoint {id:'acupoint_179', name:'神阙6', location:'前臂 3寸', method:'热敷10分钟'})
CREATE (a_180:Acupoint {id:'acupoint_180', name:'足三里7', location:'下腹部 2寸', method:'按揉16分钟'})
CREATE (a_181:Acupoint {id:'acupoint_181', name:'关元7', location:'头部 1寸', method:'艾灸18分钟'})
CREATE (a_182:Acupoint {id:'acupoint_182', name:'气海7', location:'上臂 3寸', method:'刮痧12分钟'})
CREATE (a_183:Acupoint {id:'acupoint_183', name:'中脘7', location:'上臂 5寸', method:'针刺12分钟'})
CREATE (a_184:Acupoint {id:'acupoint_184', name:'天枢7', location:'足部 2寸', method:'按揉24分钟'})
CREATE (a_185:Acupoint {id:'acupoint_185', name:'大椎7', location:'足部 4寸', method:'指压17分钟'})
CREATE (a_186:Acupoint {id:'acupoint_186', name:'命门7', location:'头部 1寸', method:'拔罐24分钟'})
CREATE (a_187:Acupoint {id:'acupoint_187', name:'肾俞7', location:'小腿外侧 3寸', method:'刮痧6分钟'})
CREATE (a_188:Acupoint {id:'acupoint_188', name:'脾俞7', location:'手部 5寸', method:'拔罐25分钟'})
CREATE (a_189:Acupoint {id:'acupoint_189', name:'肺俞7', location:'背部 2寸', method:'指压17分钟'})
CREATE (a_190:Acupoint {id:'acupoint_190', name:'心俞7', location:'上臂 3寸', method:'拔罐23分钟'})
CREATE (a_191:Acupoint {id:'acupoint_191', name:'肝俞7', location:'小腿外侧 5寸', method:'针刺16分钟'})
CREATE (a_192:Acupoint {id:'acupoint_192', name:'胆俞7', location:'前臂 2寸', method:'热敷29分钟'})
CREATE (a_193:Acupoint {id:'acupoint_193', name:'大肠俞7', location:'上臂 3寸', method:'刮痧30分钟'})
CREATE (a_194:Acupoint {id:'acupoint_194', name:'小肠俞7', location:'头部 4寸', method:'指压9分钟'})
CREATE (a_195:Acupoint {id:'acupoint_195', name:'三阴交7', location:'头部 5寸', method:'艾灸17分钟'})
CREATE (a_196:Acupoint {id:'acupoint_196', name:'阴陵泉7', location:'背部 5寸', method:'指压8分钟'})
CREATE (a_197:Acupoint {id:'acupoint_197', name:'阳陵泉7', location:'腰部 1寸', method:'刮痧28分钟'})
CREATE (a_198:Acupoint {id:'acupoint_198', name:'太溪7', location:'下腹部 4寸', method:'拔罐26分钟'})
CREATE (a_199:Acupoint {id:'acupoint_199', name:'太冲7', location:'足部 2寸', method:'针刺28分钟'})
CREATE (a_200:Acupoint {id:'acupoint_200', name:'涌泉7', location:'头部 1寸', method:'针刺25分钟'})
CREATE (a_201:Acupoint {id:'acupoint_201', name:'行间7', location:'足部 1寸', method:'针刺16分钟'})
CREATE (a_202:Acupoint {id:'acupoint_202', name:'内关7', location:'手部 3寸', method:'拔罐17分钟'})
CREATE (a_203:Acupoint {id:'acupoint_203', name:'外关7', location:'头部 2寸', method:'针刺17分钟'})
CREATE (a_204:Acupoint {id:'acupoint_204', name:'合谷7', location:'背部 3寸', method:'按揉25分钟'})
CREATE (a_205:Acupoint {id:'acupoint_205', name:'曲池7', location:'手部 3寸', method:'艾灸7分钟'})
CREATE (a_206:Acupoint {id:'acupoint_206', name:'肩井7', location:'足部 4寸', method:'指压21分钟'})
CREATE (a_207:Acupoint {id:'acupoint_207', name:'风池7', location:'头部 5寸', method:'按揉19分钟'})
CREATE (a_208:Acupoint {id:'acupoint_208', name:'百会7', location:'小腿外侧 4寸', method:'拔罐10分钟'})
CREATE (a_209:Acupoint {id:'acupoint_209', name:'神阙7', location:'前臂 3寸', method:'拔罐6分钟'})
CREATE (a_210:Acupoint {id:'acupoint_210', name:'足三里8', location:'手部 3寸', method:'热敷10分钟'})
CREATE (a_211:Acupoint {id:'acupoint_211', name:'关元8', location:'下腹部 3寸', method:'艾灸22分钟'})
CREATE (a_212:Acupoint {id:'acupoint_212', name:'气海8', location:'前臂 1寸', method:'艾灸8分钟'})
CREATE (a_213:Acupoint {id:'acupoint_213', name:'中脘8', location:'腰部 3寸', method:'热敷15分钟'})
CREATE (a_214:Acupoint {id:'acupoint_214', name:'天枢8', location:'小腿外侧 2寸', method:'指压24分钟'})
CREATE (a_215:Acupoint {id:'acupoint_215', name:'大椎8', location:'腰部 3寸', method:'指压20分钟'})
CREATE (a_216:Acupoint {id:'acupoint_216', name:'命门8', location:'足部 3寸', method:'刮痧30分钟'})
CREATE (a_217:Acupoint {id:'acupoint_217', name:'肾俞8', location:'手部 1寸', method:'刮痧9分钟'})
CREATE (a_218:Acupoint {id:'acupoint_218', name:'脾俞8', location:'背部 4寸', method:'刮痧13分钟'})
CREATE (a_219:Acupoint {id:'acupoint_219', name:'肺俞8', location:'头部 5寸', method:'热敷18分钟'})
CREATE (a_220:Acupoint {id:'acupoint_220', name:'心俞8', location:'手部 3寸', method:'拔罐12分钟'})
CREATE (a_221:Acupoint {id:'acupoint_221', name:'肝俞8', location:'上臂 4寸', method:'针刺23分钟'})
CREATE (a_222:Acupoint {id:'acupoint_222', name:'胆俞8', location:'足部 4寸', method:'艾灸15分钟'})
CREATE (a_223:Acupoint {id:'acupoint_223', name:'大肠俞8', location:'手部 1寸', method:'热敷5分钟'})
CREATE (a_224:Acupoint {id:'acupoint_224', name:'小肠俞8', location:'头部 4寸', method:'针刺22分钟'})
CREATE (a_225:Acupoint {id:'acupoint_225', name:'三阴交8', location:'背部 3寸', method:'拔罐14分钟'})
CREATE (a_226:Acupoint {id:'acupoint_226', name:'阴陵泉8', location:'手部 4寸', method:'拔罐26分钟'})
CREATE (a_227:Acupoint {id:'acupoint_227', name:'阳陵泉8', location:'下腹部 5寸', method:'指压10分钟'})
CREATE (a_228:Acupoint {id:'acupoint_228', name:'太溪8', location:'足部 4寸', method:'拔罐12分钟'})
CREATE (a_229:Acupoint {id:'acupoint_229', name:'太冲8', location:'下腹部 4寸', method:'拔罐8分钟'})
CREATE (a_230:Acupoint {id:'acupoint_230', name:'涌泉8', location:'腰部 1寸', method:'刮痧8分钟'})
CREATE (a_231:Acupoint {id:'acupoint_231', name:'行间8', location:'小腿外侧 2寸', method:'针刺25分钟'})
CREATE (a_232:Acupoint {id:'acupoint_232', name:'内关8', location:'胸部 2寸', method:'拔罐26分钟'})
CREATE (a_233:Acupoint {id:'acupoint_233', name:'外关8', location:'前臂 2寸', method:'按揉12分钟'})
CREATE (a_234:Acupoint {id:'acupoint_234', name:'合谷8', location:'前臂 1寸', method:'拔罐11分钟'})
CREATE (a_235:Acupoint {id:'acupoint_235', name:'曲池8', location:'背部 1寸', method:'热敷5分钟'})
CREATE (a_236:Acupoint {id:'acupoint_236', name:'肩井8', location:'头部 3寸', method:'热敷14分钟'})
CREATE (a_237:Acupoint {id:'acupoint_237', name:'风池8', location:'小腿外侧 5寸', method:'拔罐20分钟'})
CREATE (a_238:Acupoint {id:'acupoint_238', name:'百会8', location:'足部 3寸', method:'拔罐30分钟'})
CREATE (a_239:Acupoint {id:'acupoint_239', name:'神阙8', location:'上臂 5寸', method:'刮痧15分钟'})
CREATE (a_240:Acupoint {id:'acupoint_240', name:'足三里9', location:'上臂 4寸', method:'刮痧5分钟'})
CREATE (a_241:Acupoint {id:'acupoint_241', name:'关元9', location:'腰部 5寸', method:'按揉17分钟'})
CREATE (a_242:Acupoint {id:'acupoint_242', name:'气海9', location:'下腹部 5寸', method:'艾灸25分钟'})
CREATE (a_243:Acupoint {id:'acupoint_243', name:'中脘9', location:'背部 4寸', method:'指压19分钟'})
CREATE (a_244:Acupoint {id:'acupoint_244', name:'天枢9', location:'腰部 4寸', method:'针刺13分钟'})
CREATE (a_245:Acupoint {id:'acupoint_245', name:'大椎9', location:'背部 1寸', method:'拔罐15分钟'})
CREATE (a_246:Acupoint {id:'acupoint_246', name:'命门9', location:'上臂 3寸', method:'指压19分钟'})
CREATE (a_247:Acupoint {id:'acupoint_247', name:'肾俞9', location:'上臂 5寸', method:'指压14分钟'})
CREATE (a_248:Acupoint {id:'acupoint_248', name:'脾俞9', location:'胸部 2寸', method:'艾灸25分钟'})
CREATE (a_249:Acupoint {id:'acupoint_249', name:'肺俞9', location:'胸部 5寸', method:'拔罐6分钟'})
CREATE (a_250:Acupoint {id:'acupoint_250', name:'心俞9', location:'胸部 4寸', method:'按揉13分钟'})
CREATE (a_251:Acupoint {id:'acupoint_251', name:'肝俞9', location:'前臂 2寸', method:'指压7分钟'})
CREATE (a_252:Acupoint {id:'acupoint_252', name:'胆俞9', location:'小腿外侧 1寸', method:'指压5分钟'})
CREATE (a_253:Acupoint {id:'acupoint_253', name:'大肠俞9', location:'足部 4寸', method:'刮痧14分钟'})
CREATE (a_254:Acupoint {id:'acupoint_254', name:'小肠俞9', location:'胸部 1寸', method:'刮痧12分钟'})
CREATE (a_255:Acupoint {id:'acupoint_255', name:'三阴交9', location:'手部 3寸', method:'刮痧7分钟'})
CREATE (a_256:Acupoint {id:'acupoint_256', name:'阴陵泉9', location:'胸部 1寸', method:'按揉14分钟'})
CREATE (a_257:Acupoint {id:'acupoint_257', name:'阳陵泉9', location:'足部 4寸', method:'热敷18分钟'})
CREATE (a_258:Acupoint {id:'acupoint_258', name:'太溪9', location:'前臂 5寸', method:'按揉29分钟'})
CREATE (a_259:Acupoint {id:'acupoint_259', name:'太冲9', location:'腰部 5寸', method:'拔罐25分钟'})
CREATE (a_260:Acupoint {id:'acupoint_260', name:'涌泉9', location:'胸部 3寸', method:'拔罐27分钟'})
CREATE (a_261:Acupoint {id:'acupoint_261', name:'行间9', location:'腰部 4寸', method:'指压26分钟'})
CREATE (a_262:Acupoint {id:'acupoint_262', name:'内关9', location:'背部 1寸', method:'拔罐24分钟'})
CREATE (a_263:Acupoint {id:'acupoint_263', name:'外关9', location:'手部 4寸', method:'热敷11分钟'})
CREATE (a_264:Acupoint {id:'acupoint_264', name:'合谷9', location:'手部 5寸', method:'针刺6分钟'})
CREATE (a_265:Acupoint {id:'acupoint_265', name:'曲池9', location:'小腿外侧 2寸', method:'针刺29分钟'})
CREATE (a_266:Acupoint {id:'acupoint_266', name:'肩井9', location:'背部 3寸', method:'按揉9分钟'})
CREATE (a_267:Acupoint {id:'acupoint_267', name:'风池9', location:'腰部 2寸', method:'拔罐15分钟'})
CREATE (a_268:Acupoint {id:'acupoint_268', name:'百会9', location:'小腿外侧 1寸', method:'拔罐7分钟'})
CREATE (a_269:Acupoint {id:'acupoint_269', name:'神阙9', location:'前臂 4寸', method:'按揉28分钟'})
CREATE (a_270:Acupoint {id:'acupoint_270', name:'足三里10', location:'背部 4寸', method:'指压11分钟'})
CREATE (a_271:Acupoint {id:'acupoint_271', name:'关元10', location:'胸部 2寸', method:'拔罐12分钟'})
CREATE (a_272:Acupoint {id:'acupoint_272', name:'气海10', location:'上臂 3寸', method:'热敷13分钟'})
CREATE (a_273:Acupoint {id:'acupoint_273', name:'中脘10', location:'背部 5寸', method:'刮痧13分钟'})
CREATE (a_274:Acupoint {id:'acupoint_274', name:'天枢10', location:'前臂 5寸', method:'指压23分钟'})
CREATE (a_275:Acupoint {id:'acupoint_275', name:'大椎10', location:'头部 1寸', method:'拔罐26分钟'})
CREATE (a_276:Acupoint {id:'acupoint_276', name:'命门10', location:'前臂 4寸', method:'拔罐28分钟'})
CREATE (a_277:Acupoint {id:'acupoint_277', name:'肾俞10', location:'足部 5寸', method:'按揉19分钟'})
CREATE (a_278:Acupoint {id:'acupoint_278', name:'脾俞10', location:'小腿外侧 5寸', method:'指压11分钟'})
CREATE (a_279:Acupoint {id:'acupoint_279', name:'肺俞10', location:'足部 2寸', method:'艾灸18分钟'})
CREATE (a_280:Acupoint {id:'acupoint_280', name:'心俞10', location:'下腹部 3寸', method:'拔罐19分钟'})
CREATE (a_281:Acupoint {id:'acupoint_281', name:'肝俞10', location:'背部 5寸', method:'指压12分钟'})
CREATE (a_282:Acupoint {id:'acupoint_282', name:'胆俞10', location:'背部 2寸', method:'艾灸6分钟'})
CREATE (a_283:Acupoint {id:'acupoint_283', name:'大肠俞10', location:'头部 5寸', method:'热敷16分钟'})
CREATE (a_284:Acupoint {id:'acupoint_284', name:'小肠俞10', location:'腰部 1寸', method:'热敷30分钟'})
CREATE (a_285:Acupoint {id:'acupoint_285', name:'三阴交10', location:'头部 3寸', method:'拔罐27分钟'})
CREATE (a_286:Acupoint {id:'acupoint_286', name:'阴陵泉10', location:'手部 4寸', method:'指压10分钟'})
CREATE (a_287:Acupoint {id:'acupoint_287', name:'阳陵泉10', location:'背部 5寸', method:'指压16分钟'})
CREATE (a_288:Acupoint {id:'acupoint_288', name:'太溪10', location:'腰部 2寸', method:'指压27分钟'})
CREATE (a_289:Acupoint {id:'acupoint_289', name:'太冲10', location:'下腹部 5寸', method:'热敷7分钟'})
CREATE (a_290:Acupoint {id:'acupoint_290', name:'涌泉10', location:'上臂 4寸', method:'针刺19分钟'})
CREATE (a_291:Acupoint {id:'acupoint_291', name:'行间10', location:'前臂 2寸', method:'针刺8分钟'})
CREATE (a_292:Acupoint {id:'acupoint_292', name:'内关10', location:'小腿外侧 1寸', method:'艾灸26分钟'})
CREATE (a_293:Acupoint {id:'acupoint_293', name:'外关10', location:'头部 3寸', method:'针刺24分钟'})
CREATE (a_294:Acupoint {id:'acupoint_294', name:'合谷10', location:'下腹部 1寸', method:'指压6分钟'})
CREATE (a_295:Acupoint {id:'acupoint_295', name:'曲池10', location:'上臂 1寸', method:'刮痧29分钟'})
CREATE (a_296:Acupoint {id:'acupoint_296', name:'肩井10', location:'背部 2寸', method:'按揉8分钟'})
CREATE (a_297:Acupoint {id:'acupoint_297', name:'风池10', location:'腰部 5寸', method:'按揉8分钟'})
CREATE (a_298:Acupoint {id:'acupoint_298', name:'百会10', location:'背部 1寸', method:'艾灸14分钟'})
CREATE (a_299:Acupoint {id:'acupoint_299', name:'神阙10', location:'下腹部 3寸', method:'刮痧19分钟'})
CREATE (a_300:Acupoint {id:'acupoint_300', name:'足三里11', location:'下腹部 1寸', method:'拔罐11分钟'})
CREATE (a_301:Acupoint {id:'acupoint_301', name:'关元11', location:'上臂 4寸', method:'热敷27分钟'})
CREATE (a_302:Acupoint {id:'acupoint_302', name:'气海11', location:'腰部 4寸', method:'热敷21分钟'})
CREATE (a_303:Acupoint {id:'acupoint_303', name:'中脘11', location:'下腹部 4寸', method:'指压28分钟'})
CREATE (a_304:Acupoint {id:'acupoint_304', name:'天枢11', location:'下腹部 1寸', method:'针刺23分钟'})
CREATE (a_305:Acupoint {id:'acupoint_305', name:'大椎11', location:'腰部 1寸', method:'拔罐9分钟'})
CREATE (a_306:Acupoint {id:'acupoint_306', name:'命门11', location:'足部 5寸', method:'指压30分钟'})
CREATE (a_307:Acupoint {id:'acupoint_307', name:'肾俞11', location:'前臂 5寸', method:'指压14分钟'})
CREATE (a_308:Acupoint {id:'acupoint_308', name:'脾俞11', location:'胸部 5寸', method:'热敷20分钟'})
CREATE (a_309:Acupoint {id:'acupoint_309', name:'肺俞11', location:'手部 3寸', method:'指压13分钟'})
CREATE (a_310:Acupoint {id:'acupoint_310', name:'心俞11', location:'下腹部 1寸', method:'拔罐17分钟'})
CREATE (a_311:Acupoint {id:'acupoint_311', name:'肝俞11', location:'头部 4寸', method:'拔罐22分钟'})
CREATE (a_312:Acupoint {id:'acupoint_312', name:'胆俞11', location:'小腿外侧 3寸', method:'艾灸24分钟'})
CREATE (a_313:Acupoint {id:'acupoint_313', name:'大肠俞11', location:'前臂 5寸', method:'刮痧12分钟'})
CREATE (a_314:Acupoint {id:'acupoint_314', name:'小肠俞11', location:'下腹部 2寸', method:'拔罐11分钟'})
CREATE (a_315:Acupoint {id:'acupoint_315', name:'三阴交11', location:'胸部 3寸', method:'针刺9分钟'})
CREATE (a_316:Acupoint {id:'acupoint_316', name:'阴陵泉11', location:'背部 3寸', method:'拔罐21分钟'})
CREATE (a_317:Acupoint {id:'acupoint_317', name:'阳陵泉11', location:'足部 1寸', method:'按揉25分钟'})
CREATE (a_318:Acupoint {id:'acupoint_318', name:'太溪11', location:'背部 1寸', method:'拔罐13分钟'})
CREATE (a_319:Acupoint {id:'acupoint_319', name:'太冲11', location:'足部 4寸', method:'针刺8分钟'})
CREATE (a_320:Acupoint {id:'acupoint_320', name:'涌泉11', location:'腰部 1寸', method:'刮痧19分钟'})
CREATE (a_321:Acupoint {id:'acupoint_321', name:'行间11', location:'胸部 2寸', method:'热敷18分钟'})
CREATE (a_322:Acupoint {id:'acupoint_322', name:'内关11', location:'下腹部 2寸', method:'热敷17分钟'})
CREATE (a_323:Acupoint {id:'acupoint_323', name:'外关11', location:'腰部 2寸', method:'刮痧8分钟'})
CREATE (a_324:Acupoint {id:'acupoint_324', name:'合谷11', location:'前臂 4寸', method:'指压17分钟'})
CREATE (a_325:Acupoint {id:'acupoint_325', name:'曲池11', location:'头部 5寸', method:'拔罐12分钟'})
CREATE (a_326:Acupoint {id:'acupoint_326', name:'肩井11', location:'头部 3寸', method:'热敷12分钟'})
CREATE (a_327:Acupoint {id:'acupoint_327', name:'风池11', location:'上臂 3寸', method:'针刺26分钟'})
CREATE (a_328:Acupoint {id:'acupoint_328', name:'百会11', location:'足部 3寸', method:'刮痧25分钟'})
CREATE (a_329:Acupoint {id:'acupoint_329', name:'神阙11', location:'手部 3寸', method:'按揉14分钟'})
CREATE (a_330:Acupoint {id:'acupoint_330', name:'足三里12', location:'小腿外侧 3寸', method:'指压23分钟'})
CREATE (a_331:Acupoint {id:'acupoint_331', name:'关元12', location:'腰部 2寸', method:'指压10分钟'})
CREATE (a_332:Acupoint {id:'acupoint_332', name:'气海12', location:'手部 3寸', method:'拔罐21分钟'})
CREATE (a_333:Acupoint {id:'acupoint_333', name:'中脘12', location:'手部 2寸', method:'热敷6分钟'})
CREATE (a_334:Acupoint {id:'acupoint_334', name:'天枢12', location:'腰部 5寸', method:'针刺5分钟'})
CREATE (a_335:Acupoint {id:'acupoint_335', name:'大椎12', location:'上臂 1寸', method:'艾灸16分钟'})
CREATE (a_336:Acupoint {id:'acupoint_336', name:'命门12', location:'足部 2寸', method:'按揉27分钟'})
CREATE (a_337:Acupoint {id:'acupoint_337', name:'肾俞12', location:'手部 5寸', method:'热敷24分钟'})
CREATE (a_338:Acupoint {id:'acupoint_338', name:'脾俞12', location:'头部 2寸', method:'刮痧12分钟'})
CREATE (a_339:Acupoint {id:'acupoint_339', name:'肺俞12', location:'背部 1寸', method:'热敷18分钟'})
CREATE (a_340:Acupoint {id:'acupoint_340', name:'心俞12', location:'腰部 1寸', method:'艾灸20分钟'})
CREATE (a_341:Acupoint {id:'acupoint_341', name:'肝俞12', location:'足部 1寸', method:'拔罐29分钟'})
CREATE (a_342:Acupoint {id:'acupoint_342', name:'胆俞12', location:'足部 2寸', method:'拔罐24分钟'})
CREATE (a_343:Acupoint {id:'acupoint_343', name:'大肠俞12', location:'小腿外侧 2寸', method:'按揉15分钟'})
CREATE (a_344:Acupoint {id:'acupoint_344', name:'小肠俞12', location:'足部 5寸', method:'刮痧9分钟'})
CREATE (a_345:Acupoint {id:'acupoint_345', name:'三阴交12', location:'手部 5寸', method:'拔罐22分钟'})
CREATE (a_346:Acupoint {id:'acupoint_346', name:'阴陵泉12', location:'上臂 2寸', method:'刮痧6分钟'})
CREATE (a_347:Acupoint {id:'acupoint_347', name:'阳陵泉12', location:'足部 2寸', method:'艾灸19分钟'})
CREATE (a_348:Acupoint {id:'acupoint_348', name:'太溪12', location:'头部 3寸', method:'刮痧22分钟'})
CREATE (a_349:Acupoint {id:'acupoint_349', name:'太冲12', location:'下腹部 2寸', method:'刮痧22分钟'})
CREATE (a_350:Acupoint {id:'acupoint_350', name:'涌泉12', location:'足部 5寸', method:'拔罐11分钟'})
CREATE (a_351:Acupoint {id:'acupoint_351', name:'行间12', location:'上臂 5寸', method:'指压13分钟'})
CREATE (a_352:Acupoint {id:'acupoint_352', name:'内关12', location:'头部 3寸', method:'拔罐30分钟'})
CREATE (a_353:Acupoint {id:'acupoint_353', name:'外关12', location:'前臂 3寸', method:'热敷8分钟'})
CREATE (a_354:Acupoint {id:'acupoint_354', name:'合谷12', location:'前臂 3寸', method:'刮痧16分钟'})
CREATE (a_355:Acupoint {id:'acupoint_355', name:'曲池12', location:'手部 5寸', method:'按揉28分钟'})
CREATE (a_356:Acupoint {id:'acupoint_356', name:'肩井12', location:'下腹部 1寸', method:'针刺6分钟'})
CREATE (a_357:Acupoint {id:'acupoint_357', name:'风池12', location:'上臂 4寸', method:'按揉20分钟'})
CREATE (a_358:Acupoint {id:'acupoint_358', name:'百会12', location:'足部 5寸', method:'按揉27分钟'})
CREATE (a_359:Acupoint {id:'acupoint_359', name:'神阙12', location:'前臂 1寸', method:'针刺16分钟'})
CREATE (a_360:Acupoint {id:'acupoint_360', name:'足三里13', location:'手部 1寸', method:'艾灸7分钟'})
CREATE (a_361:Acupoint {id:'acupoint_361', name:'关元13', location:'足部 3寸', method:'按揉29分钟'})
CREATE (a_362:Acupoint {id:'acupoint_362', name:'气海13', location:'胸部 1寸', method:'针刺10分钟'})
CREATE (a_363:Acupoint {id:'acupoint_363', name:'中脘13', location:'足部 5寸', method:'按揉19分钟'})
CREATE (a_364:Acupoint {id:'acupoint_364', name:'天枢13', location:'小腿外侧 3寸', method:'热敷5分钟'})
CREATE (a_365:Acupoint {id:'acupoint_365', name:'大椎13', location:'手部 2寸', method:'针刺11分钟'})
CREATE (a_366:Acupoint {id:'acupoint_366', name:'命门13', location:'手部 5寸', method:'指压25分钟'})
CREATE (a_367:Acupoint {id:'acupoint_367', name:'肾俞13', location:'头部 4寸', method:'针刺6分钟'})
CREATE (a_368:Acupoint {id:'acupoint_368', name:'脾俞13', location:'小腿外侧 3寸', method:'热敷19分钟'})
CREATE (a_369:Acupoint {id:'acupoint_369', name:'肺俞13', location:'下腹部 5寸', method:'拔罐21分钟'})
CREATE (a_370:Acupoint {id:'acupoint_370', name:'心俞13', location:'腰部 4寸', method:'艾灸30分钟'})
CREATE (a_371:Acupoint {id:'acupoint_371', name:'肝俞13', location:'头部 1寸', method:'热敷23分钟'})
CREATE (a_372:Acupoint {id:'acupoint_372', name:'胆俞13', location:'足部 4寸', method:'按揉19分钟'})
CREATE (a_373:Acupoint {id:'acupoint_373', name:'大肠俞13', location:'手部 1寸', method:'艾灸24分钟'})
CREATE (a_374:Acupoint {id:'acupoint_374', name:'小肠俞13', location:'手部 5寸', method:'指压29分钟'})
CREATE (a_375:Acupoint {id:'acupoint_375', name:'三阴交13', location:'前臂 1寸', method:'指压12分钟'})
CREATE (a_376:Acupoint {id:'acupoint_376', name:'阴陵泉13', location:'背部 5寸', method:'针刺22分钟'})
CREATE (a_377:Acupoint {id:'acupoint_377', name:'阳陵泉13', location:'下腹部 4寸', method:'按揉21分钟'})
CREATE (a_378:Acupoint {id:'acupoint_378', name:'太溪13', location:'腰部 3寸', method:'拔罐25分钟'})
CREATE (a_379:Acupoint {id:'acupoint_379', name:'太冲13', location:'胸部 4寸', method:'艾灸29分钟'})
CREATE (a_380:Acupoint {id:'acupoint_380', name:'涌泉13', location:'头部 5寸', method:'热敷30分钟'})
CREATE (a_381:Acupoint {id:'acupoint_381', name:'行间13', location:'背部 1寸', method:'指压22分钟'})
CREATE (a_382:Acupoint {id:'acupoint_382', name:'内关13', location:'背部 3寸', method:'拔罐25分钟'})
CREATE (a_383:Acupoint {id:'acupoint_383', name:'外关13', location:'手部 5寸', method:'热敷12分钟'})
CREATE (a_384:Acupoint {id:'acupoint_384', name:'合谷13', location:'足部 3寸', method:'艾灸9分钟'})
CREATE (a_385:Acupoint {id:'acupoint_385', name:'曲池13', location:'腰部 3寸', method:'拔罐24分钟'})
CREATE (a_386:Acupoint {id:'acupoint_386', name:'肩井13', location:'足部 5寸', method:'按揉6分钟'})
CREATE (a_387:Acupoint {id:'acupoint_387', name:'风池13', location:'足部 3寸', method:'拔罐25分钟'})
CREATE (a_388:Acupoint {id:'acupoint_388', name:'百会13', location:'胸部 4寸', method:'刮痧10分钟'})
CREATE (a_389:Acupoint {id:'acupoint_389', name:'神阙13', location:'腰部 4寸', method:'按揉10分钟'})
CREATE (a_390:Acupoint {id:'acupoint_390', name:'足三里14', location:'足部 4寸', method:'拔罐18分钟'})
CREATE (a_391:Acupoint {id:'acupoint_391', name:'关元14', location:'胸部 2寸', method:'按揉30分钟'})
CREATE (a_392:Acupoint {id:'acupoint_392', name:'气海14', location:'小腿外侧 2寸', method:'拔罐5分钟'})
CREATE (a_393:Acupoint {id:'acupoint_393', name:'中脘14', location:'头部 1寸', method:'拔罐30分钟'})
CREATE (a_394:Acupoint {id:'acupoint_394', name:'天枢14', location:'上臂 5寸', method:'拔罐8分钟'})
CREATE (a_395:Acupoint {id:'acupoint_395', name:'大椎14', location:'足部 2寸', method:'针刺22分钟'})
CREATE (a_396:Acupoint {id:'acupoint_396', name:'命门14', location:'背部 1寸', method:'针刺24分钟'})
CREATE (a_397:Acupoint {id:'acupoint_397', name:'肾俞14', location:'背部 2寸', method:'按揉22分钟'})
CREATE (a_398:Acupoint {id:'acupoint_398', name:'脾俞14', location:'腰部 5寸', method:'拔罐13分钟'})
CREATE (a_399:Acupoint {id:'acupoint_399', name:'肺俞14', location:'胸部 3寸', method:'拔罐25分钟'})
CREATE (a_400:Acupoint {id:'acupoint_400', name:'心俞14', location:'小腿外侧 2寸', method:'热敷17分钟'})
CREATE (a_401:Acupoint {id:'acupoint_401', name:'肝俞14', location:'小腿外侧 3寸', method:'热敷28分钟'})
CREATE (a_402:Acupoint {id:'acupoint_402', name:'胆俞14', location:'背部 3寸', method:'按揉5分钟'})
CREATE (a_403:Acupoint {id:'acupoint_403', name:'大肠俞14', location:'小腿外侧 5寸', method:'拔罐29分钟'})
CREATE (a_404:Acupoint {id:'acupoint_404', name:'小肠俞14', location:'胸部 5寸', method:'刮痧27分钟'})
CREATE (a_405:Acupoint {id:'acupoint_405', name:'三阴交14', location:'背部 5寸', method:'针刺16分钟'})
CREATE (a_406:Acupoint {id:'acupoint_406', name:'阴陵泉14', location:'小腿外侧 3寸', method:'针刺6分钟'})
CREATE (a_407:Acupoint {id:'acupoint_407', name:'阳陵泉14', location:'足部 4寸', method:'艾灸12分钟'})
CREATE (a_408:Acupoint {id:'acupoint_408', name:'太溪14', location:'头部 5寸', method:'艾灸27分钟'})
CREATE (a_409:Acupoint {id:'acupoint_409', name:'太冲14', location:'胸部 1寸', method:'艾灸10分钟'})
CREATE (a_410:Acupoint {id:'acupoint_410', name:'涌泉14', location:'头部 4寸', method:'按揉18分钟'})
CREATE (a_411:Acupoint {id:'acupoint_411', name:'行间14', location:'上臂 4寸', method:'指压21分钟'})
CREATE (a_412:Acupoint {id:'acupoint_412', name:'内关14', location:'手部 3寸', method:'按揉18分钟'})
CREATE (a_413:Acupoint {id:'acupoint_413', name:'外关14', location:'手部 2寸', method:'指压10分钟'})
CREATE (a_414:Acupoint {id:'acupoint_414', name:'合谷14', location:'头部 4寸', method:'指压17分钟'})
CREATE (a_415:Acupoint {id:'acupoint_415', name:'曲池14', location:'手部 3寸', method:'针刺26分钟'})
CREATE (a_416:Acupoint {id:'acupoint_416', name:'肩井14', location:'背部 2寸', method:'指压26分钟'})
CREATE (a_417:Acupoint {id:'acupoint_417', name:'风池14', location:'足部 3寸', method:'按揉27分钟'})
CREATE (a_418:Acupoint {id:'acupoint_418', name:'百会14', location:'足部 1寸', method:'指压26分钟'})
CREATE (a_419:Acupoint {id:'acupoint_419', name:'神阙14', location:'足部 3寸', method:'指压19分钟'})
CREATE (a_420:Acupoint {id:'acupoint_420', name:'足三里15', location:'足部 5寸', method:'拔罐18分钟'})
CREATE (a_421:Acupoint {id:'acupoint_421', name:'关元15', location:'下腹部 1寸', method:'指压9分钟'})
CREATE (a_422:Acupoint {id:'acupoint_422', name:'气海15', location:'上臂 2寸', method:'针刺23分钟'})
CREATE (a_423:Acupoint {id:'acupoint_423', name:'中脘15', location:'前臂 5寸', method:'按揉17分钟'})
CREATE (a_424:Acupoint {id:'acupoint_424', name:'天枢15', location:'背部 1寸', method:'艾灸28分钟'})
CREATE (a_425:Acupoint {id:'acupoint_425', name:'大椎15', location:'头部 4寸', method:'热敷21分钟'})
CREATE (a_426:Acupoint {id:'acupoint_426', name:'命门15', location:'足部 3寸', method:'针刺28分钟'})
CREATE (a_427:Acupoint {id:'acupoint_427', name:'肾俞15', location:'上臂 3寸', method:'热敷5分钟'})
CREATE (a_428:Acupoint {id:'acupoint_428', name:'脾俞15', location:'背部 5寸', method:'按揉19分钟'})
CREATE (a_429:Acupoint {id:'acupoint_429', name:'肺俞15', location:'胸部 5寸', method:'热敷11分钟'})
CREATE (a_430:Acupoint {id:'acupoint_430', name:'心俞15', location:'足部 3寸', method:'针刺24分钟'})
CREATE (a_431:Acupoint {id:'acupoint_431', name:'肝俞15', location:'上臂 3寸', method:'艾灸21分钟'})
CREATE (a_432:Acupoint {id:'acupoint_432', name:'胆俞15', location:'腰部 4寸', method:'拔罐23分钟'})
CREATE (a_433:Acupoint {id:'acupoint_433', name:'大肠俞15', location:'上臂 4寸', method:'刮痧30分钟'})
CREATE (a_434:Acupoint {id:'acupoint_434', name:'小肠俞15', location:'小腿外侧 4寸', method:'指压24分钟'})
CREATE (a_435:Acupoint {id:'acupoint_435', name:'三阴交15', location:'小腿外侧 5寸', method:'指压30分钟'})
CREATE (a_436:Acupoint {id:'acupoint_436', name:'阴陵泉15', location:'手部 2寸', method:'针刺19分钟'})
CREATE (a_437:Acupoint {id:'acupoint_437', name:'阳陵泉15', location:'小腿外侧 5寸', method:'拔罐17分钟'})
CREATE (a_438:Acupoint {id:'acupoint_438', name:'太溪15', location:'小腿外侧 4寸', method:'热敷20分钟'})
CREATE (a_439:Acupoint {id:'acupoint_439', name:'太冲15', location:'胸部 5寸', method:'刮痧28分钟'})
CREATE (a_440:Acupoint {id:'acupoint_440', name:'涌泉15', location:'腰部 2寸', method:'艾灸9分钟'})
CREATE (a_441:Acupoint {id:'acupoint_441', name:'行间15', location:'下腹部 4寸', method:'拔罐26分钟'})
CREATE (a_442:Acupoint {id:'acupoint_442', name:'内关15', location:'腰部 3寸', method:'指压9分钟'})
CREATE (a_443:Acupoint {id:'acupoint_443', name:'外关15', location:'头部 1寸', method:'指压28分钟'})
CREATE (a_444:Acupoint {id:'acupoint_444', name:'合谷15', location:'手部 4寸', method:'拔罐21分钟'})
CREATE (a_445:Acupoint {id:'acupoint_445', name:'曲池15', location:'手部 2寸', method:'针刺11分钟'})
CREATE (a_446:Acupoint {id:'acupoint_446', name:'肩井15', location:'足部 2寸', method:'按揉23分钟'})
CREATE (a_447:Acupoint {id:'acupoint_447', name:'风池15', location:'前臂 3寸', method:'热敷28分钟'})
CREATE (a_448:Acupoint {id:'acupoint_448', name:'百会15', location:'前臂 1寸', method:'艾灸23分钟'})
CREATE (a_449:Acupoint {id:'acupoint_449', name:'神阙15', location:'头部 4寸', method:'针刺21分钟'})
CREATE (a_450:Acupoint {id:'acupoint_450', name:'足三里16', location:'胸部 3寸', method:'热敷15分钟'})
CREATE (a_451:Acupoint {id:'acupoint_451', name:'关元16', location:'上臂 1寸', method:'按揉29分钟'})
CREATE (a_452:Acupoint {id:'acupoint_452', name:'气海16', location:'头部 3寸', method:'指压13分钟'})
CREATE (a_453:Acupoint {id:'acupoint_453', name:'中脘16', location:'背部 3寸', method:'指压16分钟'})
CREATE (a_454:Acupoint {id:'acupoint_454', name:'天枢16', location:'上臂 1寸', method:'艾灸5分钟'})
CREATE (a_455:Acupoint {id:'acupoint_455', name:'大椎16', location:'上臂 5寸', method:'按揉5分钟'})
CREATE (a_456:Acupoint {id:'acupoint_456', name:'命门16', location:'腰部 5寸', method:'针刺10分钟'})
CREATE (a_457:Acupoint {id:'acupoint_457', name:'肾俞16', location:'上臂 2寸', method:'指压12分钟'})
CREATE (a_458:Acupoint {id:'acupoint_458', name:'脾俞16', location:'胸部 2寸', method:'按揉17分钟'})
CREATE (a_459:Acupoint {id:'acupoint_459', name:'肺俞16', location:'下腹部 4寸', method:'刮痧10分钟'})
CREATE (a_460:Acupoint {id:'acupoint_460', name:'心俞16', location:'背部 2寸', method:'指压29分钟'})
CREATE (a_461:Acupoint {id:'acupoint_461', name:'肝俞16', location:'手部 2寸', method:'拔罐6分钟'})
CREATE (a_462:Acupoint {id:'acupoint_462', name:'胆俞16', location:'胸部 2寸', method:'指压6分钟'})
CREATE (a_463:Acupoint {id:'acupoint_463', name:'大肠俞16', location:'小腿外侧 3寸', method:'按揉13分钟'})
CREATE (a_464:Acupoint {id:'acupoint_464', name:'小肠俞16', location:'足部 4寸', method:'刮痧8分钟'})
CREATE (a_465:Acupoint {id:'acupoint_465', name:'三阴交16', location:'胸部 2寸', method:'艾灸19分钟'})
CREATE (a_466:Acupoint {id:'acupoint_466', name:'阴陵泉16', location:'头部 3寸', method:'刮痧9分钟'})
CREATE (a_467:Acupoint {id:'acupoint_467', name:'阳陵泉16', location:'手部 5寸', method:'热敷8分钟'})
CREATE (a_468:Acupoint {id:'acupoint_468', name:'太溪16', location:'背部 1寸', method:'热敷30分钟'})
CREATE (a_469:Acupoint {id:'acupoint_469', name:'太冲16', location:'头部 3寸', method:'指压8分钟'})
CREATE (a_470:Acupoint {id:'acupoint_470', name:'涌泉16', location:'上臂 1寸', method:'指压24分钟'})
CREATE (a_471:Acupoint {id:'acupoint_471', name:'行间16', location:'足部 2寸', method:'拔罐7分钟'})
CREATE (a_472:Acupoint {id:'acupoint_472', name:'内关16', location:'手部 4寸', method:'热敷23分钟'})
CREATE (a_473:Acupoint {id:'acupoint_473', name:'外关16', location:'前臂 1寸', method:'指压11分钟'})
CREATE (a_474:Acupoint {id:'acupoint_474', name:'合谷16', location:'手部 2寸', method:'拔罐23分钟'})
CREATE (a_475:Acupoint {id:'acupoint_475', name:'曲池16', location:'足部 2寸', method:'指压23分钟'})
CREATE (a_476:Acupoint {id:'acupoint_476', name:'肩井16', location:'足部 2寸', method:'拔罐17分钟'})
CREATE (a_477:Acupoint {id:'acupoint_477', name:'风池16', location:'小腿外侧 5寸', method:'艾灸7分钟'})
CREATE (a_478:Acupoint {id:'acupoint_478', name:'百会16', location:'上臂 4寸', method:'艾灸17分钟'})
CREATE (a_479:Acupoint {id:'acupoint_479', name:'神阙16', location:'上臂 3寸', method:'艾灸28分钟'})
CREATE (a_480:Acupoint {id:'acupoint_480', name:'足三里17', location:'下腹部 5寸', method:'刮痧6分钟'})
CREATE (a_481:Acupoint {id:'acupoint_481', name:'关元17', location:'上臂 5寸', method:'按揉19分钟'})
CREATE (a_482:Acupoint {id:'acupoint_482', name:'气海17', location:'前臂 1寸', method:'指压18分钟'})
CREATE (a_483:Acupoint {id:'acupoint_483', name:'中脘17', location:'下腹部 5寸', method:'针刺25分钟'})
CREATE (a_484:Acupoint {id:'acupoint_484', name:'天枢17', location:'上臂 1寸', method:'刮痧16分钟'})
CREATE (a_485:Acupoint {id:'acupoint_485', name:'大椎17', location:'下腹部 4寸', method:'艾灸19分钟'})
CREATE (a_486:Acupoint {id:'acupoint_486', name:'命门17', location:'头部 1寸', method:'指压19分钟'})
CREATE (a_487:Acupoint {id:'acupoint_487', name:'肾俞17', location:'胸部 2寸', method:'艾灸14分钟'})
CREATE (a_488:Acupoint {id:'acupoint_488', name:'脾俞17', location:'足部 3寸', method:'热敷22分钟'})
CREATE (a_489:Acupoint {id:'acupoint_489', name:'肺俞17', location:'下腹部 1寸', method:'针刺16分钟'})
CREATE (a_490:Acupoint {id:'acupoint_490', name:'心俞17', location:'前臂 5寸', method:'艾灸12分钟'})
CREATE (a_491:Acupoint {id:'acupoint_491', name:'肝俞17', location:'背部 4寸', method:'热敷30分钟'})
CREATE (a_492:Acupoint {id:'acupoint_492', name:'胆俞17', location:'下腹部 5寸', method:'艾灸7分钟'})
CREATE (a_493:Acupoint {id:'acupoint_493', name:'大肠俞17', location:'头部 1寸', method:'指压27分钟'})
CREATE (a_494:Acupoint {id:'acupoint_494', name:'小肠俞17', location:'前臂 5寸', method:'针刺22分钟'})
CREATE (a_495:Acupoint {id:'acupoint_495', name:'三阴交17', location:'下腹部 2寸', method:'指压12分钟'})
CREATE (a_496:Acupoint {id:'acupoint_496', name:'阴陵泉17', location:'腰部 1寸', method:'刮痧8分钟'})
CREATE (a_497:Acupoint {id:'acupoint_497', name:'阳陵泉17', location:'腰部 5寸', method:'热敷19分钟'})
CREATE (a_498:Acupoint {id:'acupoint_498', name:'太溪17', location:'小腿外侧 1寸', method:'刮痧23分钟'})
CREATE (a_499:Acupoint {id:'acupoint_499', name:'太冲17', location:'前臂 4寸', method:'拔罐23分钟'})
CREATE (f_0:Food {id:'food_0', name:'山药', nature:'凉', effect:'养胃、止泻'})
CREATE (f_1:Food {id:'food_1', name:'薏米', nature:'凉', effect:'化痰、化痰'})
CREATE (f_2:Food {id:'food_2', name:'红豆', nature:'热', effect:'行气、止泻'})
CREATE (f_3:Food {id:'food_3', name:'绿豆', nature:'寒', effect:'行气、滋阴'})
CREATE (f_4:Food {id:'food_4', name:'黑豆', nature:'凉', effect:'止咳、清热'})
CREATE (f_5:Food {id:'food_5', name:'黄豆', nature:'微温', effect:'祛湿、通便'})
CREATE (f_6:Food {id:'food_6', name:'小米', nature:'平', effect:'解毒、安神'})
CREATE (f_7:Food {id:'food_7', name:'大米', nature:'温', effect:'止咳、止泻'})
CREATE (f_8:Food {id:'food_8', name:'糯米', nature:'微温', effect:'补肾、化瘀'})
CREATE (f_9:Food {id:'food_9', name:'小麦', nature:'微温', effect:'通便、止咳'})
CREATE (f_10:Food {id:'food_10', name:'大麦', nature:'温', effect:'化瘀、解郁'})
CREATE (f_11:Food {id:'food_11', name:'燕麦', nature:'寒', effect:'补肾、安神'})
CREATE (f_12:Food {id:'food_12', name:'荞麦', nature:'平', effect:'清热、活血'})
CREATE (f_13:Food {id:'food_13', name:'玉米', nature:'平', effect:'滋阴、壮阳'})
CREATE (f_14:Food {id:'food_14', name:'红薯', nature:'温', effect:'解毒、通便'})
CREATE (f_15:Food {id:'food_15', name:'土豆', nature:'寒', effect:'止泻、安神'})
CREATE (f_16:Food {id:'food_16', name:'芋头', nature:'温', effect:'健脾、清热'})
CREATE (f_17:Food {id:'food_17', name:'莲藕', nature:'温', effect:'化痰、化痰'})
CREATE (f_18:Food {id:'food_18', name:'百合', nature:'热', effect:'清热、行气'})
CREATE (f_19:Food {id:'food_19', name:'银耳', nature:'微温', effect:'健脾、安神'})
CREATE (f_20:Food {id:'food_20', name:'木耳', nature:'微寒', effect:'行气、通便'})
CREATE (f_21:Food {id:'food_21', name:'香菇', nature:'微寒', effect:'补气、止泻'})
CREATE (f_22:Food {id:'food_22', name:'蘑菇', nature:'温', effect:'补血、止咳'})
CREATE (f_23:Food {id:'food_23', name:'金针菇', nature:'寒', effect:'祛湿、补血'})
CREATE (f_24:Food {id:'food_24', name:'猴头菇', nature:'凉', effect:'止泻、解毒'})
CREATE (f_25:Food {id:'food_25', name:'红枣', nature:'凉', effect:'通便、补气'})
CREATE (f_26:Food {id:'food_26', name:'枸杞', nature:'平', effect:'养胃、滋阴'})
CREATE (f_27:Food {id:'food_27', name:'桂圆', nature:'温', effect:'补气、健脾'})
CREATE (f_28:Food {id:'food_28', name:'莲子', nature:'微温', effect:'补气、补血'})
CREATE (f_29:Food {id:'food_29', name:'芡实', nature:'微温', effect:'通便、润肺'})
CREATE (f_30:Food {id:'food_30', name:'茯苓', nature:'微寒', effect:'解毒、行气'})
CREATE (f_31:Food {id:'food_31', name:'白术', nature:'微寒', effect:'祛湿、健脾'})
CREATE (f_32:Food {id:'food_32', name:'党参', nature:'热', effect:'行气、壮阳'})
CREATE (f_33:Food {id:'food_33', name:'黄芪', nature:'平', effect:'解毒、健脾'})
CREATE (f_34:Food {id:'food_34', name:'当归', nature:'寒', effect:'解毒、补气'})
CREATE (f_35:Food {id:'food_35', name:'熟地', nature:'凉', effect:'行气、壮阳'})
CREATE (f_36:Food {id:'food_36', name:'白芍', nature:'温', effect:'活血、通便'})
CREATE (f_37:Food {id:'food_37', name:'川芎', nature:'寒', effect:'通便、行气'})
CREATE (f_38:Food {id:'food_38', name:'丹参', nature:'温', effect:'解郁、壮阳'})
CREATE (f_39:Food {id:'food_39', name:'山楂', nature:'微温', effect:'补肾、补气'})
CREATE (f_40:Food {id:'food_40', name:'陈皮', nature:'温', effect:'壮阳、健脾'})
CREATE (f_41:Food {id:'food_41', name:'生姜', nature:'热', effect:'活血、壮阳'})
CREATE (f_42:Food {id:'food_42', name:'大葱', nature:'寒', effect:'化瘀、润肺'})
CREATE (f_43:Food {id:'food_43', name:'大蒜', nature:'凉', effect:'活血、清热'})
CREATE (f_44:Food {id:'food_44', name:'肉桂', nature:'热', effect:'活血、补血'})
CREATE (f_45:Food {id:'food_45', name:'花椒', nature:'微寒', effect:'解毒、祛湿'})
CREATE (f_46:Food {id:'food_46', name:'小茴香', nature:'微寒', effect:'养胃、活血'})
CREATE (f_47:Food {id:'food_47', name:'山药2', nature:'微温', effect:'化痰、解毒'})
CREATE (f_48:Food {id:'food_48', name:'薏米2', nature:'温', effect:'清热、健脾'})
CREATE (f_49:Food {id:'food_49', name:'红豆2', nature:'温', effect:'行气、润肺'})
CREATE (f_50:Food {id:'food_50', name:'绿豆2', nature:'寒', effect:'化瘀、补血'})
CREATE (f_51:Food {id:'food_51', name:'黑豆2', nature:'微寒', effect:'补血、止咳'})
CREATE (f_52:Food {id:'food_52', name:'黄豆2', nature:'平', effect:'活血、止咳'})
CREATE (f_53:Food {id:'food_53', name:'小米2', nature:'寒', effect:'解毒、补气'})
CREATE (f_54:Food {id:'food_54', name:'大米2', nature:'温', effect:'祛湿、解毒'})
CREATE (f_55:Food {id:'food_55', name:'糯米2', nature:'微温', effect:'活血、滋阴'})
CREATE (f_56:Food {id:'food_56', name:'小麦2', nature:'凉', effect:'祛湿、止泻'})
CREATE (f_57:Food {id:'food_57', name:'大麦2', nature:'微寒', effect:'化瘀、补气'})
CREATE (f_58:Food {id:'food_58', name:'燕麦2', nature:'热', effect:'通便、通便'})
CREATE (f_59:Food {id:'food_59', name:'荞麦2', nature:'微温', effect:'健脾、滋阴'})
CREATE (f_60:Food {id:'food_60', name:'玉米2', nature:'温', effect:'解毒、止泻'})
CREATE (f_61:Food {id:'food_61', name:'红薯2', nature:'凉', effect:'化瘀、通便'})
CREATE (f_62:Food {id:'food_62', name:'土豆2', nature:'热', effect:'化瘀、通便'})
CREATE (f_63:Food {id:'food_63', name:'芋头2', nature:'凉', effect:'壮阳、补肾'})
CREATE (f_64:Food {id:'food_64', name:'莲藕2', nature:'平', effect:'补肾、安神'})
CREATE (f_65:Food {id:'food_65', name:'百合2', nature:'凉', effect:'壮阳、解毒'})
CREATE (f_66:Food {id:'food_66', name:'银耳2', nature:'微寒', effect:'滋阴、清热'})
CREATE (f_67:Food {id:'food_67', name:'木耳2', nature:'平', effect:'补肾、滋阴'})
CREATE (f_68:Food {id:'food_68', name:'香菇2', nature:'温', effect:'止咳、止咳'})
CREATE (f_69:Food {id:'food_69', name:'蘑菇2', nature:'热', effect:'养胃、祛湿'})
CREATE (f_70:Food {id:'food_70', name:'金针菇2', nature:'热', effect:'补血、润肺'})
CREATE (f_71:Food {id:'food_71', name:'猴头菇2', nature:'微寒', effect:'健脾、通便'})
CREATE (f_72:Food {id:'food_72', name:'红枣2', nature:'温', effect:'解郁、活血'})
CREATE (f_73:Food {id:'food_73', name:'枸杞2', nature:'微寒', effect:'清热、止泻'})
CREATE (f_74:Food {id:'food_74', name:'桂圆2', nature:'寒', effect:'健脾、活血'})
CREATE (f_75:Food {id:'food_75', name:'莲子2', nature:'寒', effect:'行气、解毒'})
CREATE (f_76:Food {id:'food_76', name:'芡实2', nature:'热', effect:'止咳、补肾'})
CREATE (f_77:Food {id:'food_77', name:'茯苓2', nature:'凉', effect:'通便、化瘀'})
CREATE (f_78:Food {id:'food_78', name:'白术2', nature:'热', effect:'润肺、祛湿'})
CREATE (f_79:Food {id:'food_79', name:'党参2', nature:'寒', effect:'安神、润肺'})
CREATE (f_80:Food {id:'food_80', name:'黄芪2', nature:'微寒', effect:'滋阴、健脾'})
CREATE (f_81:Food {id:'food_81', name:'当归2', nature:'热', effect:'补气、补血'})
CREATE (f_82:Food {id:'food_82', name:'熟地2', nature:'微寒', effect:'祛湿、健脾'})
CREATE (f_83:Food {id:'food_83', name:'白芍2', nature:'微寒', effect:'健脾、补气'})
CREATE (f_84:Food {id:'food_84', name:'川芎2', nature:'微温', effect:'通便、化痰'})
CREATE (f_85:Food {id:'food_85', name:'丹参2', nature:'微温', effect:'活血、通便'})
CREATE (f_86:Food {id:'food_86', name:'山楂2', nature:'平', effect:'安神、止咳'})
CREATE (f_87:Food {id:'food_87', name:'陈皮2', nature:'微寒', effect:'健脾、壮阳'})
CREATE (f_88:Food {id:'food_88', name:'生姜2', nature:'微温', effect:'解毒、安神'})
CREATE (f_89:Food {id:'food_89', name:'大葱2', nature:'微寒', effect:'祛湿、补气'})
CREATE (f_90:Food {id:'food_90', name:'大蒜2', nature:'温', effect:'补气、清热'})
CREATE (f_91:Food {id:'food_91', name:'肉桂2', nature:'温', effect:'壮阳、清热'})
CREATE (f_92:Food {id:'food_92', name:'花椒2', nature:'温', effect:'润肺、养胃'})
CREATE (f_93:Food {id:'food_93', name:'小茴香2', nature:'微温', effect:'清热、行气'})
CREATE (f_94:Food {id:'food_94', name:'山药3', nature:'微温', effect:'清热、行气'})
CREATE (f_95:Food {id:'food_95', name:'薏米3', nature:'微温', effect:'润肺、润肺'})
CREATE (f_96:Food {id:'food_96', name:'红豆3', nature:'热', effect:'补血、壮阳'})
CREATE (f_97:Food {id:'food_97', name:'绿豆3', nature:'平', effect:'养胃、清热'})
CREATE (f_98:Food {id:'food_98', name:'黑豆3', nature:'热', effect:'补肾、安神'})
CREATE (f_99:Food {id:'food_99', name:'黄豆3', nature:'寒', effect:'行气、安神'})
CREATE (f_100:Food {id:'food_100', name:'小米3', nature:'微寒', effect:'补肾、养胃'})
CREATE (f_101:Food {id:'food_101', name:'大米3', nature:'微寒', effect:'壮阳、润肺'})
CREATE (f_102:Food {id:'food_102', name:'糯米3', nature:'寒', effect:'健脾、祛湿'})
CREATE (f_103:Food {id:'food_103', name:'小麦3', nature:'热', effect:'化痰、解郁'})
CREATE (f_104:Food {id:'food_104', name:'大麦3', nature:'微寒', effect:'化瘀、解郁'})
CREATE (f_105:Food {id:'food_105', name:'燕麦3', nature:'温', effect:'安神、补肾'})
CREATE (f_106:Food {id:'food_106', name:'荞麦3', nature:'寒', effect:'养胃、祛湿'})
CREATE (f_107:Food {id:'food_107', name:'玉米3', nature:'凉', effect:'通便、润肺'})
CREATE (f_108:Food {id:'food_108', name:'红薯3', nature:'热', effect:'解郁、补血'})
CREATE (f_109:Food {id:'food_109', name:'土豆3', nature:'微温', effect:'健脾、补气'})
CREATE (f_110:Food {id:'food_110', name:'芋头3', nature:'温', effect:'通便、补气'})
CREATE (f_111:Food {id:'food_111', name:'莲藕3', nature:'凉', effect:'活血、止泻'})
CREATE (f_112:Food {id:'food_112', name:'百合3', nature:'微温', effect:'止咳、通便'})
CREATE (f_113:Food {id:'food_113', name:'银耳3', nature:'寒', effect:'化痰、补肾'})
CREATE (f_114:Food {id:'food_114', name:'木耳3', nature:'寒', effect:'健脾、止咳'})
CREATE (f_115:Food {id:'food_115', name:'香菇3', nature:'微寒', effect:'安神、祛湿'})
CREATE (f_116:Food {id:'food_116', name:'蘑菇3', nature:'微温', effect:'润肺、补肾'})
CREATE (f_117:Food {id:'food_117', name:'金针菇3', nature:'寒', effect:'止咳、行气'})
CREATE (f_118:Food {id:'food_118', name:'猴头菇3', nature:'平', effect:'健脾、解毒'})
CREATE (f_119:Food {id:'food_119', name:'红枣3', nature:'凉', effect:'补气、解郁'})
CREATE (f_120:Food {id:'food_120', name:'枸杞3', nature:'微寒', effect:'清热、补肾'})
CREATE (f_121:Food {id:'food_121', name:'桂圆3', nature:'温', effect:'养胃、健脾'})
CREATE (f_122:Food {id:'food_122', name:'莲子3', nature:'热', effect:'养胃、滋阴'})
CREATE (f_123:Food {id:'food_123', name:'芡实3', nature:'寒', effect:'补肾、止咳'})
CREATE (f_124:Food {id:'food_124', name:'茯苓3', nature:'微寒', effect:'通便、解郁'})
CREATE (f_125:Food {id:'food_125', name:'白术3', nature:'寒', effect:'化痰、润肺'})
CREATE (f_126:Food {id:'food_126', name:'党参3', nature:'寒', effect:'祛湿、养胃'})
CREATE (f_127:Food {id:'food_127', name:'黄芪3', nature:'微温', effect:'止泻、清热'})
CREATE (f_128:Food {id:'food_128', name:'当归3', nature:'寒', effect:'壮阳、补气'})
CREATE (f_129:Food {id:'food_129', name:'熟地3', nature:'微温', effect:'润肺、养胃'})
CREATE (f_130:Food {id:'food_130', name:'白芍3', nature:'热', effect:'祛湿、化瘀'})
CREATE (f_131:Food {id:'food_131', name:'川芎3', nature:'微温', effect:'壮阳、安神'})
CREATE (f_132:Food {id:'food_132', name:'丹参3', nature:'微温', effect:'祛湿、养胃'})
CREATE (f_133:Food {id:'food_133', name:'山楂3', nature:'微寒', effect:'化瘀、润肺'})
CREATE (f_134:Food {id:'food_134', name:'陈皮3', nature:'凉', effect:'化瘀、补血'})
CREATE (f_135:Food {id:'food_135', name:'生姜3', nature:'微寒', effect:'通便、清热'})
CREATE (f_136:Food {id:'food_136', name:'大葱3', nature:'温', effect:'健脾、解毒'})
CREATE (f_137:Food {id:'food_137', name:'大蒜3', nature:'微温', effect:'行气、健脾'})
CREATE (f_138:Food {id:'food_138', name:'肉桂3', nature:'寒', effect:'健脾、止泻'})
CREATE (f_139:Food {id:'food_139', name:'花椒3', nature:'热', effect:'补肾、行气'})
CREATE (f_140:Food {id:'food_140', name:'小茴香3', nature:'温', effect:'止咳、解毒'})
CREATE (f_141:Food {id:'food_141', name:'山药4', nature:'微温', effect:'活血、解毒'})
CREATE (f_142:Food {id:'food_142', name:'薏米4', nature:'温', effect:'祛湿、润肺'})
CREATE (f_143:Food {id:'food_143', name:'红豆4', nature:'平', effect:'补肾、补血'})
CREATE (f_144:Food {id:'food_144', name:'绿豆4', nature:'凉', effect:'健脾、滋阴'})
CREATE (f_145:Food {id:'food_145', name:'黑豆4', nature:'微寒', effect:'补血、通便'})
CREATE (f_146:Food {id:'food_146', name:'黄豆4', nature:'平', effect:'行气、化痰'})
CREATE (f_147:Food {id:'food_147', name:'小米4', nature:'热', effect:'清热、化痰'})
CREATE (f_148:Food {id:'food_148', name:'大米4', nature:'温', effect:'壮阳、活血'})
CREATE (f_149:Food {id:'food_149', name:'糯米4', nature:'微温', effect:'解郁、养胃'})
CREATE (f_150:Food {id:'food_150', name:'小麦4', nature:'凉', effect:'通便、健脾'})
CREATE (f_151:Food {id:'food_151', name:'大麦4', nature:'微温', effect:'止泻、行气'})
CREATE (f_152:Food {id:'food_152', name:'燕麦4', nature:'寒', effect:'止泻、化瘀'})
CREATE (f_153:Food {id:'food_153', name:'荞麦4', nature:'热', effect:'止泻、安神'})
CREATE (f_154:Food {id:'food_154', name:'玉米4', nature:'寒', effect:'止咳、清热'})
CREATE (f_155:Food {id:'food_155', name:'红薯4', nature:'热', effect:'安神、活血'})
CREATE (f_156:Food {id:'food_156', name:'土豆4', nature:'微寒', effect:'壮阳、止咳'})
CREATE (f_157:Food {id:'food_157', name:'芋头4', nature:'温', effect:'健脾、补血'})
CREATE (f_158:Food {id:'food_158', name:'莲藕4', nature:'微寒', effect:'健脾、解毒'})
CREATE (f_159:Food {id:'food_159', name:'百合4', nature:'微温', effect:'解郁、解郁'})
CREATE (f_160:Food {id:'food_160', name:'银耳4', nature:'微寒', effect:'通便、滋阴'})
CREATE (f_161:Food {id:'food_161', name:'木耳4', nature:'微温', effect:'安神、补肾'})
CREATE (f_162:Food {id:'food_162', name:'香菇4', nature:'微温', effect:'补血、通便'})
CREATE (f_163:Food {id:'food_163', name:'蘑菇4', nature:'温', effect:'化瘀、补气'})
CREATE (f_164:Food {id:'food_164', name:'金针菇4', nature:'平', effect:'养胃、化痰'})
CREATE (f_165:Food {id:'food_165', name:'猴头菇4', nature:'微温', effect:'通便、解毒'})
CREATE (f_166:Food {id:'food_166', name:'红枣4', nature:'平', effect:'清热、祛湿'})
CREATE (f_167:Food {id:'food_167', name:'枸杞4', nature:'微温', effect:'润肺、祛湿'})
CREATE (f_168:Food {id:'food_168', name:'桂圆4', nature:'平', effect:'补肾、祛湿'})
CREATE (f_169:Food {id:'food_169', name:'莲子4', nature:'寒', effect:'祛湿、通便'})
CREATE (f_170:Food {id:'food_170', name:'芡实4', nature:'微温', effect:'补血、补肾'})
CREATE (f_171:Food {id:'food_171', name:'茯苓4', nature:'凉', effect:'止咳、养胃'})
CREATE (f_172:Food {id:'food_172', name:'白术4', nature:'温', effect:'祛湿、行气'})
CREATE (f_173:Food {id:'food_173', name:'党参4', nature:'热', effect:'通便、止咳'})
CREATE (f_174:Food {id:'food_174', name:'黄芪4', nature:'寒', effect:'养胃、安神'})
CREATE (f_175:Food {id:'food_175', name:'当归4', nature:'平', effect:'化痰、补肾'})
CREATE (f_176:Food {id:'food_176', name:'熟地4', nature:'温', effect:'健脾、止泻'})
CREATE (f_177:Food {id:'food_177', name:'白芍4', nature:'寒', effect:'补肾、补血'})
CREATE (f_178:Food {id:'food_178', name:'川芎4', nature:'平', effect:'清热、补血'})
CREATE (f_179:Food {id:'food_179', name:'丹参4', nature:'寒', effect:'祛湿、通便'})
CREATE (f_180:Food {id:'food_180', name:'山楂4', nature:'凉', effect:'补血、化瘀'})
CREATE (f_181:Food {id:'food_181', name:'陈皮4', nature:'微温', effect:'安神、解毒'})
CREATE (f_182:Food {id:'food_182', name:'生姜4', nature:'凉', effect:'化瘀、祛湿'})
CREATE (f_183:Food {id:'food_183', name:'大葱4', nature:'平', effect:'解毒、补气'})
CREATE (f_184:Food {id:'food_184', name:'大蒜4', nature:'平', effect:'壮阳、化瘀'})
CREATE (f_185:Food {id:'food_185', name:'肉桂4', nature:'微温', effect:'补肾、养胃'})
CREATE (f_186:Food {id:'food_186', name:'花椒4', nature:'热', effect:'补血、养胃'})
CREATE (f_187:Food {id:'food_187', name:'小茴香4', nature:'凉', effect:'补气、祛湿'})
CREATE (f_188:Food {id:'food_188', name:'山药5', nature:'凉', effect:'止咳、化痰'})
CREATE (f_189:Food {id:'food_189', name:'薏米5', nature:'温', effect:'通便、止泻'})
CREATE (f_190:Food {id:'food_190', name:'红豆5', nature:'微寒', effect:'养胃、补肾'})
CREATE (f_191:Food {id:'food_191', name:'绿豆5', nature:'平', effect:'止泻、行气'})
CREATE (f_192:Food {id:'food_192', name:'黑豆5', nature:'热', effect:'活血、解郁'})
CREATE (f_193:Food {id:'food_193', name:'黄豆5', nature:'凉', effect:'补肾、化瘀'})
CREATE (f_194:Food {id:'food_194', name:'小米5', nature:'平', effect:'补肾、解毒'})
CREATE (f_195:Food {id:'food_195', name:'大米5', nature:'平', effect:'补血、安神'})
CREATE (f_196:Food {id:'food_196', name:'糯米5', nature:'凉', effect:'解毒、清热'})
CREATE (f_197:Food {id:'food_197', name:'小麦5', nature:'热', effect:'化痰、健脾'})
CREATE (f_198:Food {id:'food_198', name:'大麦5', nature:'微寒', effect:'解郁、活血'})
CREATE (f_199:Food {id:'food_199', name:'燕麦5', nature:'热', effect:'壮阳、健脾'})
CREATE (f_200:Food {id:'food_200', name:'荞麦5', nature:'热', effect:'化瘀、通便'})
CREATE (f_201:Food {id:'food_201', name:'玉米5', nature:'温', effect:'清热、补血'})
CREATE (f_202:Food {id:'food_202', name:'红薯5', nature:'微寒', effect:'安神、止泻'})
CREATE (f_203:Food {id:'food_203', name:'土豆5', nature:'温', effect:'壮阳、化痰'})
CREATE (f_204:Food {id:'food_204', name:'芋头5', nature:'热', effect:'止咳、健脾'})
CREATE (f_205:Food {id:'food_205', name:'莲藕5', nature:'微温', effect:'健脾、壮阳'})
CREATE (f_206:Food {id:'food_206', name:'百合5', nature:'寒', effect:'健脾、化瘀'})
CREATE (f_207:Food {id:'food_207', name:'银耳5', nature:'凉', effect:'滋阴、健脾'})
CREATE (f_208:Food {id:'food_208', name:'木耳5', nature:'微寒', effect:'化瘀、壮阳'})
CREATE (f_209:Food {id:'food_209', name:'香菇5', nature:'平', effect:'健脾、壮阳'})
CREATE (f_210:Food {id:'food_210', name:'蘑菇5', nature:'微寒', effect:'止泻、补气'})
CREATE (f_211:Food {id:'food_211', name:'金针菇5', nature:'微寒', effect:'壮阳、解毒'})
CREATE (f_212:Food {id:'food_212', name:'猴头菇5', nature:'微温', effect:'壮阳、通便'})
CREATE (f_213:Food {id:'food_213', name:'红枣5', nature:'寒', effect:'健脾、补血'})
CREATE (f_214:Food {id:'food_214', name:'枸杞5', nature:'温', effect:'祛湿、健脾'})
CREATE (f_215:Food {id:'food_215', name:'桂圆5', nature:'热', effect:'清热、通便'})
CREATE (f_216:Food {id:'food_216', name:'莲子5', nature:'寒', effect:'解郁、解郁'})
CREATE (f_217:Food {id:'food_217', name:'芡实5', nature:'温', effect:'补气、健脾'})
CREATE (f_218:Food {id:'food_218', name:'茯苓5', nature:'温', effect:'化瘀、补肾'})
CREATE (f_219:Food {id:'food_219', name:'白术5', nature:'热', effect:'活血、解郁'})
CREATE (f_220:Food {id:'food_220', name:'党参5', nature:'凉', effect:'养胃、补肾'})
CREATE (f_221:Food {id:'food_221', name:'黄芪5', nature:'热', effect:'补气、止咳'})
CREATE (f_222:Food {id:'food_222', name:'当归5', nature:'平', effect:'补气、养胃'})
CREATE (f_223:Food {id:'food_223', name:'熟地5', nature:'微寒', effect:'祛湿、活血'})
CREATE (f_224:Food {id:'food_224', name:'白芍5', nature:'微温', effect:'化痰、补血'})
CREATE (f_225:Food {id:'food_225', name:'川芎5', nature:'微寒', effect:'清热、滋阴'})
CREATE (f_226:Food {id:'food_226', name:'丹参5', nature:'凉', effect:'清热、化瘀'})
CREATE (f_227:Food {id:'food_227', name:'山楂5', nature:'凉', effect:'润肺、化痰'})
CREATE (f_228:Food {id:'food_228', name:'陈皮5', nature:'寒', effect:'活血、安神'})
CREATE (f_229:Food {id:'food_229', name:'生姜5', nature:'寒', effect:'润肺、活血'})
CREATE (f_230:Food {id:'food_230', name:'大葱5', nature:'温', effect:'止泻、活血'})
CREATE (f_231:Food {id:'food_231', name:'大蒜5', nature:'热', effect:'通便、化瘀'})
CREATE (f_232:Food {id:'food_232', name:'肉桂5', nature:'平', effect:'通便、滋阴'})
CREATE (f_233:Food {id:'food_233', name:'花椒5', nature:'平', effect:'补气、养胃'})
CREATE (f_234:Food {id:'food_234', name:'小茴香5', nature:'微温', effect:'养胃、润肺'})
CREATE (f_235:Food {id:'food_235', name:'山药6', nature:'微寒', effect:'补气、安神'})
CREATE (f_236:Food {id:'food_236', name:'薏米6', nature:'凉', effect:'养胃、补血'})
CREATE (f_237:Food {id:'food_237', name:'红豆6', nature:'热', effect:'补气、化瘀'})
CREATE (f_238:Food {id:'food_238', name:'绿豆6', nature:'微寒', effect:'化痰、化痰'})
CREATE (f_239:Food {id:'food_239', name:'黑豆6', nature:'温', effect:'壮阳、通便'})
CREATE (f_240:Food {id:'food_240', name:'黄豆6', nature:'寒', effect:'清热、活血'})
CREATE (f_241:Food {id:'food_241', name:'小米6', nature:'温', effect:'养胃、安神'})
CREATE (f_242:Food {id:'food_242', name:'大米6', nature:'微寒', effect:'养胃、清热'})
CREATE (f_243:Food {id:'food_243', name:'糯米6', nature:'微寒', effect:'补肾、止咳'})
CREATE (f_244:Food {id:'food_244', name:'小麦6', nature:'寒', effect:'健脾、壮阳'})
CREATE (f_245:Food {id:'food_245', name:'大麦6', nature:'凉', effect:'解郁、安神'})
CREATE (f_246:Food {id:'food_246', name:'燕麦6', nature:'微寒', effect:'止泻、解毒'})
CREATE (f_247:Food {id:'food_247', name:'荞麦6', nature:'寒', effect:'补血、补肾'})
CREATE (f_248:Food {id:'food_248', name:'玉米6', nature:'微寒', effect:'壮阳、祛湿'})
CREATE (f_249:Food {id:'food_249', name:'红薯6', nature:'寒', effect:'壮阳、壮阳'})
CREATE (f_250:Food {id:'food_250', name:'土豆6', nature:'微温', effect:'止咳、通便'})
CREATE (f_251:Food {id:'food_251', name:'芋头6', nature:'热', effect:'祛湿、健脾'})
CREATE (f_252:Food {id:'food_252', name:'莲藕6', nature:'微温', effect:'行气、活血'})
CREATE (f_253:Food {id:'food_253', name:'百合6', nature:'温', effect:'活血、通便'})
CREATE (f_254:Food {id:'food_254', name:'银耳6', nature:'微寒', effect:'解郁、安神'})
CREATE (f_255:Food {id:'food_255', name:'木耳6', nature:'凉', effect:'化痰、养胃'})
CREATE (f_256:Food {id:'food_256', name:'香菇6', nature:'凉', effect:'祛湿、止咳'})
CREATE (f_257:Food {id:'food_257', name:'蘑菇6', nature:'热', effect:'解毒、补血'})
CREATE (f_258:Food {id:'food_258', name:'金针菇6', nature:'微温', effect:'补气、通便'})
CREATE (f_259:Food {id:'food_259', name:'猴头菇6', nature:'凉', effect:'解郁、壮阳'})
CREATE (f_260:Food {id:'food_260', name:'红枣6', nature:'平', effect:'化瘀、补气'})
CREATE (f_261:Food {id:'food_261', name:'枸杞6', nature:'平', effect:'补肾、止泻'})
CREATE (f_262:Food {id:'food_262', name:'桂圆6', nature:'微寒', effect:'补血、滋阴'})
CREATE (f_263:Food {id:'food_263', name:'莲子6', nature:'温', effect:'活血、解郁'})
CREATE (f_264:Food {id:'food_264', name:'芡实6', nature:'热', effect:'行气、补气'})
CREATE (f_265:Food {id:'food_265', name:'茯苓6', nature:'凉', effect:'滋阴、止咳'})
CREATE (f_266:Food {id:'food_266', name:'白术6', nature:'寒', effect:'止泻、补气'})
CREATE (f_267:Food {id:'food_267', name:'党参6', nature:'寒', effect:'化痰、通便'})
CREATE (f_268:Food {id:'food_268', name:'黄芪6', nature:'微温', effect:'壮阳、安神'})
CREATE (f_269:Food {id:'food_269', name:'当归6', nature:'平', effect:'行气、滋阴'})
CREATE (f_270:Food {id:'food_270', name:'熟地6', nature:'平', effect:'健脾、化痰'})
CREATE (f_271:Food {id:'food_271', name:'白芍6', nature:'凉', effect:'化瘀、安神'})
CREATE (f_272:Food {id:'food_272', name:'川芎6', nature:'寒', effect:'通便、解毒'})
CREATE (f_273:Food {id:'food_273', name:'丹参6', nature:'微温', effect:'止咳、健脾'})
CREATE (f_274:Food {id:'food_274', name:'山楂6', nature:'微寒', effect:'壮阳、补血'})
CREATE (f_275:Food {id:'food_275', name:'陈皮6', nature:'热', effect:'通便、止咳'})
CREATE (f_276:Food {id:'food_276', name:'生姜6', nature:'微寒', effect:'止泻、活血'})
CREATE (f_277:Food {id:'food_277', name:'大葱6', nature:'微温', effect:'通便、化痰'})
CREATE (f_278:Food {id:'food_278', name:'大蒜6', nature:'平', effect:'补血、滋阴'})
CREATE (f_279:Food {id:'food_279', name:'肉桂6', nature:'凉', effect:'化瘀、补血'})
CREATE (f_280:Food {id:'food_280', name:'花椒6', nature:'温', effect:'补气、解郁'})
CREATE (f_281:Food {id:'food_281', name:'小茴香6', nature:'微寒', effect:'滋阴、润肺'})
CREATE (f_282:Food {id:'food_282', name:'山药7', nature:'微寒', effect:'通便、健脾'})
CREATE (f_283:Food {id:'food_283', name:'薏米7', nature:'平', effect:'润肺、化痰'})
CREATE (f_284:Food {id:'food_284', name:'红豆7', nature:'热', effect:'解毒、解毒'})
CREATE (f_285:Food {id:'food_285', name:'绿豆7', nature:'微温', effect:'润肺、解郁'})
CREATE (f_286:Food {id:'food_286', name:'黑豆7', nature:'凉', effect:'解郁、补血'})
CREATE (f_287:Food {id:'food_287', name:'黄豆7', nature:'热', effect:'安神、壮阳'})
CREATE (f_288:Food {id:'food_288', name:'小米7', nature:'寒', effect:'健脾、化痰'})
CREATE (f_289:Food {id:'food_289', name:'大米7', nature:'微寒', effect:'健脾、清热'})
CREATE (f_290:Food {id:'food_290', name:'糯米7', nature:'平', effect:'化瘀、解毒'})
CREATE (f_291:Food {id:'food_291', name:'小麦7', nature:'热', effect:'行气、滋阴'})
CREATE (f_292:Food {id:'food_292', name:'大麦7', nature:'热', effect:'补血、化痰'})
CREATE (f_293:Food {id:'food_293', name:'燕麦7', nature:'凉', effect:'解郁、养胃'})
CREATE (f_294:Food {id:'food_294', name:'荞麦7', nature:'微温', effect:'祛湿、健脾'})
CREATE (f_295:Food {id:'food_295', name:'玉米7', nature:'温', effect:'解毒、化痰'})
CREATE (f_296:Food {id:'food_296', name:'红薯7', nature:'温', effect:'补血、壮阳'})
CREATE (f_297:Food {id:'food_297', name:'土豆7', nature:'热', effect:'润肺、滋阴'})
CREATE (f_298:Food {id:'food_298', name:'芋头7', nature:'微寒', effect:'止咳、解郁'})
CREATE (f_299:Food {id:'food_299', name:'莲藕7', nature:'微温', effect:'化痰、清热'})
CREATE (f_300:Food {id:'food_300', name:'百合7', nature:'微寒', effect:'解郁、祛湿'})
CREATE (f_301:Food {id:'food_301', name:'银耳7', nature:'平', effect:'清热、壮阳'})
CREATE (f_302:Food {id:'food_302', name:'木耳7', nature:'寒', effect:'补肾、养胃'})
CREATE (f_303:Food {id:'food_303', name:'香菇7', nature:'微温', effect:'润肺、清热'})
CREATE (f_304:Food {id:'food_304', name:'蘑菇7', nature:'温', effect:'滋阴、补肾'})
CREATE (f_305:Food {id:'food_305', name:'金针菇7', nature:'寒', effect:'化痰、养胃'})
CREATE (f_306:Food {id:'food_306', name:'猴头菇7', nature:'微温', effect:'补气、健脾'})
CREATE (f_307:Food {id:'food_307', name:'红枣7', nature:'微温', effect:'滋阴、活血'})
CREATE (f_308:Food {id:'food_308', name:'枸杞7', nature:'微温', effect:'滋阴、润肺'})
CREATE (f_309:Food {id:'food_309', name:'桂圆7', nature:'微寒', effect:'安神、通便'})
CREATE (f_310:Food {id:'food_310', name:'莲子7', nature:'热', effect:'解郁、养胃'})
CREATE (f_311:Food {id:'food_311', name:'芡实7', nature:'平', effect:'通便、补气'})
CREATE (f_312:Food {id:'food_312', name:'茯苓7', nature:'温', effect:'滋阴、健脾'})
CREATE (f_313:Food {id:'food_313', name:'白术7', nature:'寒', effect:'止咳、养胃'})
CREATE (f_314:Food {id:'food_314', name:'党参7', nature:'温', effect:'解毒、健脾'})
CREATE (f_315:Food {id:'food_315', name:'黄芪7', nature:'凉', effect:'壮阳、止咳'})
CREATE (f_316:Food {id:'food_316', name:'当归7', nature:'凉', effect:'安神、解郁'})
CREATE (f_317:Food {id:'food_317', name:'熟地7', nature:'温', effect:'止泻、行气'})
CREATE (f_318:Food {id:'food_318', name:'白芍7', nature:'寒', effect:'止咳、化痰'})
CREATE (f_319:Food {id:'food_319', name:'川芎7', nature:'微寒', effect:'解毒、解郁'})
CREATE (f_320:Food {id:'food_320', name:'丹参7', nature:'温', effect:'解郁、止泻'})
CREATE (f_321:Food {id:'food_321', name:'山楂7', nature:'凉', effect:'养胃、止泻'})
CREATE (f_322:Food {id:'food_322', name:'陈皮7', nature:'寒', effect:'祛湿、活血'})
CREATE (f_323:Food {id:'food_323', name:'生姜7', nature:'凉', effect:'止咳、清热'})
CREATE (f_324:Food {id:'food_324', name:'大葱7', nature:'微寒', effect:'止咳、补气'})
CREATE (f_325:Food {id:'food_325', name:'大蒜7', nature:'平', effect:'止咳、活血'})
CREATE (f_326:Food {id:'food_326', name:'肉桂7', nature:'寒', effect:'健脾、安神'})
CREATE (f_327:Food {id:'food_327', name:'花椒7', nature:'微温', effect:'祛湿、壮阳'})
CREATE (f_328:Food {id:'food_328', name:'小茴香7', nature:'微寒', effect:'壮阳、壮阳'})
CREATE (f_329:Food {id:'food_329', name:'山药8', nature:'热', effect:'解郁、清热'})
CREATE (f_330:Food {id:'food_330', name:'薏米8', nature:'平', effect:'滋阴、行气'})
CREATE (f_331:Food {id:'food_331', name:'红豆8', nature:'温', effect:'健脾、止泻'})
CREATE (f_332:Food {id:'food_332', name:'绿豆8', nature:'微温', effect:'行气、润肺'})
CREATE (f_333:Food {id:'food_333', name:'黑豆8', nature:'寒', effect:'止泻、健脾'})
CREATE (f_334:Food {id:'food_334', name:'黄豆8', nature:'热', effect:'化痰、滋阴'})
CREATE (f_335:Food {id:'food_335', name:'小米8', nature:'热', effect:'止泻、化痰'})
CREATE (f_336:Food {id:'food_336', name:'大米8', nature:'微寒', effect:'化瘀、活血'})
CREATE (f_337:Food {id:'food_337', name:'糯米8', nature:'微温', effect:'止咳、润肺'})
CREATE (f_338:Food {id:'food_338', name:'小麦8', nature:'微温', effect:'补血、活血'})
CREATE (f_339:Food {id:'food_339', name:'大麦8', nature:'微温', effect:'健脾、化痰'})
CREATE (f_340:Food {id:'food_340', name:'燕麦8', nature:'寒', effect:'补气、润肺'})
CREATE (f_341:Food {id:'food_341', name:'荞麦8', nature:'凉', effect:'补血、止咳'})
CREATE (f_342:Food {id:'food_342', name:'玉米8', nature:'微温', effect:'健脾、补血'})
CREATE (f_343:Food {id:'food_343', name:'红薯8', nature:'平', effect:'补肾、活血'})
CREATE (f_344:Food {id:'food_344', name:'土豆8', nature:'热', effect:'滋阴、止泻'})
CREATE (f_345:Food {id:'food_345', name:'芋头8', nature:'微寒', effect:'壮阳、清热'})
CREATE (f_346:Food {id:'food_346', name:'莲藕8', nature:'凉', effect:'清热、补气'})
CREATE (f_347:Food {id:'food_347', name:'百合8', nature:'热', effect:'补气、养胃'})
CREATE (f_348:Food {id:'food_348', name:'银耳8', nature:'凉', effect:'化痰、通便'})
CREATE (f_349:Food {id:'food_349', name:'木耳8', nature:'热', effect:'清热、止泻'})
CREATE (f_350:Food {id:'food_350', name:'香菇8', nature:'温', effect:'安神、解毒'})
CREATE (f_351:Food {id:'food_351', name:'蘑菇8', nature:'温', effect:'通便、解毒'})
CREATE (f_352:Food {id:'food_352', name:'金针菇8', nature:'凉', effect:'补气、止泻'})
CREATE (f_353:Food {id:'food_353', name:'猴头菇8', nature:'寒', effect:'祛湿、补气'})
CREATE (f_354:Food {id:'food_354', name:'红枣8', nature:'平', effect:'活血、解郁'})
CREATE (f_355:Food {id:'food_355', name:'枸杞8', nature:'寒', effect:'补肾、润肺'})
CREATE (f_356:Food {id:'food_356', name:'桂圆8', nature:'微寒', effect:'通便、补肾'})
CREATE (f_357:Food {id:'food_357', name:'莲子8', nature:'微寒', effect:'解毒、养胃'})
CREATE (f_358:Food {id:'food_358', name:'芡实8', nature:'平', effect:'清热、止咳'})
CREATE (f_359:Food {id:'food_359', name:'茯苓8', nature:'温', effect:'补气、清热'})
CREATE (f_360:Food {id:'food_360', name:'白术8', nature:'凉', effect:'祛湿、解毒'})
CREATE (f_361:Food {id:'food_361', name:'党参8', nature:'寒', effect:'补血、祛湿'})
CREATE (f_362:Food {id:'food_362', name:'黄芪8', nature:'微温', effect:'安神、活血'})
CREATE (f_363:Food {id:'food_363', name:'当归8', nature:'微温', effect:'祛湿、壮阳'})
CREATE (f_364:Food {id:'food_364', name:'熟地8', nature:'寒', effect:'补血、润肺'})
CREATE (f_365:Food {id:'food_365', name:'白芍8', nature:'微寒', effect:'化瘀、止泻'})
CREATE (f_366:Food {id:'food_366', name:'川芎8', nature:'温', effect:'解郁、通便'})
CREATE (f_367:Food {id:'food_367', name:'丹参8', nature:'凉', effect:'止咳、化痰'})
CREATE (f_368:Food {id:'food_368', name:'山楂8', nature:'微寒', effect:'补血、补肾'})
CREATE (f_369:Food {id:'food_369', name:'陈皮8', nature:'平', effect:'解郁、润肺'})
CREATE (f_370:Food {id:'food_370', name:'生姜8', nature:'微寒', effect:'通便、解郁'})
CREATE (f_371:Food {id:'food_371', name:'大葱8', nature:'寒', effect:'清热、解郁'})
CREATE (f_372:Food {id:'food_372', name:'大蒜8', nature:'温', effect:'润肺、解毒'})
CREATE (f_373:Food {id:'food_373', name:'肉桂8', nature:'微温', effect:'健脾、清热'})
CREATE (f_374:Food {id:'food_374', name:'花椒8', nature:'平', effect:'补血、化瘀'})
CREATE (f_375:Food {id:'food_375', name:'小茴香8', nature:'平', effect:'壮阳、养胃'})
CREATE (f_376:Food {id:'food_376', name:'山药9', nature:'热', effect:'补血、壮阳'})
CREATE (f_377:Food {id:'food_377', name:'薏米9', nature:'寒', effect:'补肾、补血'})
CREATE (f_378:Food {id:'food_378', name:'红豆9', nature:'平', effect:'安神、补血'})
CREATE (f_379:Food {id:'food_379', name:'绿豆9', nature:'温', effect:'补气、润肺'})
CREATE (f_380:Food {id:'food_380', name:'黑豆9', nature:'凉', effect:'止泻、安神'})
CREATE (f_381:Food {id:'food_381', name:'黄豆9', nature:'平', effect:'行气、祛湿'})
CREATE (f_382:Food {id:'food_382', name:'小米9', nature:'微温', effect:'安神、补肾'})
CREATE (f_383:Food {id:'food_383', name:'大米9', nature:'微寒', effect:'壮阳、补气'})
CREATE (f_384:Food {id:'food_384', name:'糯米9', nature:'微温', effect:'行气、解毒'})
CREATE (f_385:Food {id:'food_385', name:'小麦9', nature:'平', effect:'滋阴、润肺'})
CREATE (f_386:Food {id:'food_386', name:'大麦9', nature:'寒', effect:'滋阴、止咳'})
CREATE (f_387:Food {id:'food_387', name:'燕麦9', nature:'微寒', effect:'止泻、行气'})
CREATE (f_388:Food {id:'food_388', name:'荞麦9', nature:'热', effect:'解毒、补血'})
CREATE (f_389:Food {id:'food_389', name:'玉米9', nature:'微温', effect:'解毒、止咳'})
CREATE (f_390:Food {id:'food_390', name:'红薯9', nature:'微寒', effect:'解毒、壮阳'})
CREATE (f_391:Food {id:'food_391', name:'土豆9', nature:'凉', effect:'健脾、止泻'})
CREATE (f_392:Food {id:'food_392', name:'芋头9', nature:'微温', effect:'补血、活血'})
CREATE (f_393:Food {id:'food_393', name:'莲藕9', nature:'热', effect:'行气、解郁'})
CREATE (f_394:Food {id:'food_394', name:'百合9', nature:'寒', effect:'止咳、止咳'})
CREATE (f_395:Food {id:'food_395', name:'银耳9', nature:'凉', effect:'解毒、活血'})
CREATE (f_396:Food {id:'food_396', name:'木耳9', nature:'平', effect:'清热、安神'})
CREATE (f_397:Food {id:'food_397', name:'香菇9', nature:'寒', effect:'补血、活血'})
CREATE (f_398:Food {id:'food_398', name:'蘑菇9', nature:'微温', effect:'健脾、健脾'})
CREATE (f_399:Food {id:'food_399', name:'金针菇9', nature:'微寒', effect:'滋阴、壮阳'})
CREATE (f_400:Food {id:'food_400', name:'猴头菇9', nature:'微寒', effect:'补血、壮阳'})
CREATE (f_401:Food {id:'food_401', name:'红枣9', nature:'微温', effect:'壮阳、止咳'})
CREATE (f_402:Food {id:'food_402', name:'枸杞9', nature:'微温', effect:'化痰、活血'})
CREATE (f_403:Food {id:'food_403', name:'桂圆9', nature:'热', effect:'补血、养胃'})
CREATE (f_404:Food {id:'food_404', name:'莲子9', nature:'微温', effect:'止咳、止咳'})
CREATE (f_405:Food {id:'food_405', name:'芡实9', nature:'平', effect:'活血、解郁'})
CREATE (f_406:Food {id:'food_406', name:'茯苓9', nature:'热', effect:'通便、化痰'})
CREATE (f_407:Food {id:'food_407', name:'白术9', nature:'温', effect:'补气、滋阴'})
CREATE (f_408:Food {id:'food_408', name:'党参9', nature:'热', effect:'行气、化瘀'})
CREATE (f_409:Food {id:'food_409', name:'黄芪9', nature:'温', effect:'行气、补肾'})
CREATE (f_410:Food {id:'food_410', name:'当归9', nature:'平', effect:'滋阴、健脾'})
CREATE (f_411:Food {id:'food_411', name:'熟地9', nature:'热', effect:'通便、健脾'})
CREATE (f_412:Food {id:'food_412', name:'白芍9', nature:'平', effect:'通便、壮阳'})
CREATE (f_413:Food {id:'food_413', name:'川芎9', nature:'寒', effect:'行气、祛湿'})
CREATE (f_414:Food {id:'food_414', name:'丹参9', nature:'凉', effect:'活血、滋阴'})
CREATE (f_415:Food {id:'food_415', name:'山楂9', nature:'寒', effect:'滋阴、止泻'})
CREATE (f_416:Food {id:'food_416', name:'陈皮9', nature:'平', effect:'润肺、止泻'})
CREATE (f_417:Food {id:'food_417', name:'生姜9', nature:'微温', effect:'滋阴、养胃'})
CREATE (f_418:Food {id:'food_418', name:'大葱9', nature:'微寒', effect:'活血、健脾'})
CREATE (f_419:Food {id:'food_419', name:'大蒜9', nature:'热', effect:'祛湿、养胃'})
CREATE (f_420:Food {id:'food_420', name:'肉桂9', nature:'热', effect:'祛湿、解郁'})
CREATE (f_421:Food {id:'food_421', name:'花椒9', nature:'温', effect:'安神、壮阳'})
CREATE (f_422:Food {id:'food_422', name:'小茴香9', nature:'微寒', effect:'健脾、行气'})
CREATE (f_423:Food {id:'food_423', name:'山药10', nature:'平', effect:'健脾、化痰'})
CREATE (f_424:Food {id:'food_424', name:'薏米10', nature:'热', effect:'补肾、清热'})
CREATE (f_425:Food {id:'food_425', name:'红豆10', nature:'温', effect:'止泻、健脾'})
CREATE (f_426:Food {id:'food_426', name:'绿豆10', nature:'凉', effect:'润肺、补肾'})
CREATE (f_427:Food {id:'food_427', name:'黑豆10', nature:'微温', effect:'行气、补血'})
CREATE (f_428:Food {id:'food_428', name:'黄豆10', nature:'热', effect:'通便、安神'})
CREATE (f_429:Food {id:'food_429', name:'小米10', nature:'寒', effect:'养胃、祛湿'})
CREATE (f_430:Food {id:'food_430', name:'大米10', nature:'凉', effect:'通便、壮阳'})
CREATE (f_431:Food {id:'food_431', name:'糯米10', nature:'寒', effect:'润肺、祛湿'})
CREATE (f_432:Food {id:'food_432', name:'小麦10', nature:'温', effect:'化痰、止咳'})
CREATE (f_433:Food {id:'food_433', name:'大麦10', nature:'热', effect:'化瘀、祛湿'})
CREATE (f_434:Food {id:'food_434', name:'燕麦10', nature:'微寒', effect:'养胃、行气'})
CREATE (f_435:Food {id:'food_435', name:'荞麦10', nature:'凉', effect:'清热、行气'})
CREATE (f_436:Food {id:'food_436', name:'玉米10', nature:'微温', effect:'化瘀、化痰'})
CREATE (f_437:Food {id:'food_437', name:'红薯10', nature:'热', effect:'补血、解郁'})
CREATE (f_438:Food {id:'food_438', name:'土豆10', nature:'平', effect:'补肾、解郁'})
CREATE (f_439:Food {id:'food_439', name:'芋头10', nature:'温', effect:'止咳、润肺'})
CREATE (f_440:Food {id:'food_440', name:'莲藕10', nature:'微寒', effect:'润肺、止泻'})
CREATE (f_441:Food {id:'food_441', name:'百合10', nature:'微寒', effect:'通便、化瘀'})
CREATE (f_442:Food {id:'food_442', name:'银耳10', nature:'寒', effect:'补血、壮阳'})
CREATE (f_443:Food {id:'food_443', name:'木耳10', nature:'凉', effect:'化痰、补肾'})
CREATE (f_444:Food {id:'food_444', name:'香菇10', nature:'平', effect:'健脾、壮阳'})
CREATE (f_445:Food {id:'food_445', name:'蘑菇10', nature:'寒', effect:'化痰、壮阳'})
CREATE (f_446:Food {id:'food_446', name:'金针菇10', nature:'平', effect:'解毒、通便'})
CREATE (f_447:Food {id:'food_447', name:'猴头菇10', nature:'微温', effect:'祛湿、补血'})
CREATE (f_448:Food {id:'food_448', name:'红枣10', nature:'热', effect:'润肺、祛湿'})
CREATE (f_449:Food {id:'food_449', name:'枸杞10', nature:'微寒', effect:'滋阴、解郁'})
CREATE (f_450:Food {id:'food_450', name:'桂圆10', nature:'微寒', effect:'通便、解郁'})
CREATE (f_451:Food {id:'food_451', name:'莲子10', nature:'凉', effect:'止咳、壮阳'})
CREATE (f_452:Food {id:'food_452', name:'芡实10', nature:'寒', effect:'补血、止咳'})
CREATE (f_453:Food {id:'food_453', name:'茯苓10', nature:'微寒', effect:'滋阴、化瘀'})
CREATE (f_454:Food {id:'food_454', name:'白术10', nature:'平', effect:'活血、解毒'})
CREATE (f_455:Food {id:'food_455', name:'党参10', nature:'微温', effect:'通便、补血'})
CREATE (f_456:Food {id:'food_456', name:'黄芪10', nature:'寒', effect:'滋阴、养胃'})
CREATE (f_457:Food {id:'food_457', name:'当归10', nature:'热', effect:'解毒、止泻'})
CREATE (f_458:Food {id:'food_458', name:'熟地10', nature:'凉', effect:'通便、通便'})
CREATE (f_459:Food {id:'food_459', name:'白芍10', nature:'温', effect:'补肾、解毒'})
CREATE (f_460:Food {id:'food_460', name:'川芎10', nature:'微寒', effect:'化瘀、行气'})
CREATE (f_461:Food {id:'food_461', name:'丹参10', nature:'寒', effect:'清热、止泻'})
CREATE (f_462:Food {id:'food_462', name:'山楂10', nature:'温', effect:'补气、养胃'})
CREATE (f_463:Food {id:'food_463', name:'陈皮10', nature:'温', effect:'化痰、润肺'})
CREATE (f_464:Food {id:'food_464', name:'生姜10', nature:'微温', effect:'化痰、健脾'})
CREATE (f_465:Food {id:'food_465', name:'大葱10', nature:'凉', effect:'解毒、止咳'})
CREATE (f_466:Food {id:'food_466', name:'大蒜10', nature:'平', effect:'行气、化痰'})
CREATE (f_467:Food {id:'food_467', name:'肉桂10', nature:'平', effect:'行气、壮阳'})
CREATE (f_468:Food {id:'food_468', name:'花椒10', nature:'微寒', effect:'补肾、祛湿'})
CREATE (f_469:Food {id:'food_469', name:'小茴香10', nature:'凉', effect:'解郁、行气'})
CREATE (f_470:Food {id:'food_470', name:'山药11', nature:'温', effect:'祛湿、解郁'})
CREATE (f_471:Food {id:'food_471', name:'薏米11', nature:'平', effect:'止泻、补肾'})
CREATE (f_472:Food {id:'food_472', name:'红豆11', nature:'微温', effect:'壮阳、补血'})
CREATE (f_473:Food {id:'food_473', name:'绿豆11', nature:'温', effect:'止泻、行气'})
CREATE (f_474:Food {id:'food_474', name:'黑豆11', nature:'微寒', effect:'壮阳、补肾'})
CREATE (f_475:Food {id:'food_475', name:'黄豆11', nature:'寒', effect:'通便、补血'})
CREATE (f_476:Food {id:'food_476', name:'小米11', nature:'微温', effect:'通便、补气'})
CREATE (f_477:Food {id:'food_477', name:'大米11', nature:'凉', effect:'止咳、清热'})
CREATE (f_478:Food {id:'food_478', name:'糯米11', nature:'凉', effect:'解毒、活血'})
CREATE (f_479:Food {id:'food_479', name:'小麦11', nature:'凉', effect:'祛湿、润肺'})
CREATE (f_480:Food {id:'food_480', name:'大麦11', nature:'寒', effect:'清热、滋阴'})
CREATE (f_481:Food {id:'food_481', name:'燕麦11', nature:'微寒', effect:'行气、活血'})
CREATE (f_482:Food {id:'food_482', name:'荞麦11', nature:'寒', effect:'行气、补气'})
CREATE (f_483:Food {id:'food_483', name:'玉米11', nature:'微温', effect:'补气、解郁'})
CREATE (f_484:Food {id:'food_484', name:'红薯11', nature:'微寒', effect:'壮阳、止泻'})
CREATE (f_485:Food {id:'food_485', name:'土豆11', nature:'热', effect:'健脾、通便'})
CREATE (f_486:Food {id:'food_486', name:'芋头11', nature:'微寒', effect:'安神、清热'})
CREATE (f_487:Food {id:'food_487', name:'莲藕11', nature:'平', effect:'通便、行气'})
CREATE (f_488:Food {id:'food_488', name:'百合11', nature:'寒', effect:'解毒、活血'})
CREATE (f_489:Food {id:'food_489', name:'银耳11', nature:'微温', effect:'润肺、补肾'})
CREATE (f_490:Food {id:'food_490', name:'木耳11', nature:'微寒', effect:'补血、活血'})
CREATE (f_491:Food {id:'food_491', name:'香菇11', nature:'平', effect:'通便、化瘀'})
CREATE (f_492:Food {id:'food_492', name:'蘑菇11', nature:'寒', effect:'祛湿、解毒'})
CREATE (f_493:Food {id:'food_493', name:'金针菇11', nature:'平', effect:'清热、健脾'})
CREATE (f_494:Food {id:'food_494', name:'猴头菇11', nature:'微寒', effect:'化瘀、行气'})
CREATE (f_495:Food {id:'food_495', name:'红枣11', nature:'微温', effect:'解毒、祛湿'})
CREATE (f_496:Food {id:'food_496', name:'枸杞11', nature:'热', effect:'通便、补血'})
CREATE (f_497:Food {id:'food_497', name:'桂圆11', nature:'寒', effect:'安神、行气'})
CREATE (f_498:Food {id:'food_498', name:'莲子11', nature:'寒', effect:'解毒、滋阴'})
CREATE (f_499:Food {id:'food_499', name:'芡实11', nature:'微寒', effect:'活血、化瘀'})
CREATE (e_0:Exercise {id:'exercise_0', name:'八段锦', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_1:Exercise {id:'exercise_1', name:'太极拳', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_2:Exercise {id:'exercise_2', name:'五禽戏', effect:'疏通经络', method:'每周3-5次'})
CREATE (e_3:Exercise {id:'exercise_3', name:'易筋经', effect:'疏通经络', method:'每次30分钟'})
CREATE (e_4:Exercise {id:'exercise_4', name:'六字诀', effect:'舒缓压力', method:'每次20分钟'})
CREATE (e_5:Exercise {id:'exercise_5', name:'站桩', effect:'提升免疫', method:'每日1次'})
CREATE (e_6:Exercise {id:'exercise_6', name:'散步', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_7:Exercise {id:'exercise_7', name:'慢跑', effect:'增强体质', method:'饭后1小时'})
CREATE (e_8:Exercise {id:'exercise_8', name:'快走', effect:'疏通经络', method:'清晨练习'})
CREATE (e_9:Exercise {id:'exercise_9', name:'游泳', effect:'强筋健骨', method:'每周3-5次'})
CREATE (e_10:Exercise {id:'exercise_10', name:'瑜伽', effect:'调和气血', method:'傍晚练习'})
CREATE (e_11:Exercise {id:'exercise_11', name:'普拉提', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_12:Exercise {id:'exercise_12', name:'健身操', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_13:Exercise {id:'exercise_13', name:'广场舞', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_14:Exercise {id:'exercise_14', name:'跳绳', effect:'疏通经络', method:'每次30分钟'})
CREATE (e_15:Exercise {id:'exercise_15', name:'爬楼梯', effect:'强筋健骨', method:'每日1次'})
CREATE (e_16:Exercise {id:'exercise_16', name:'骑行', effect:'减肥塑形', method:'每日1次'})
CREATE (e_17:Exercise {id:'exercise_17', name:'登山', effect:'提升免疫', method:'饭后1小时'})
CREATE (e_18:Exercise {id:'exercise_18', name:'气功', effect:'强筋健骨', method:'每日1次'})
CREATE (e_19:Exercise {id:'exercise_19', name:'导引术', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_20:Exercise {id:'exercise_20', name:'八段锦2', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_21:Exercise {id:'exercise_21', name:'太极拳2', effect:'改善睡眠', method:'每次30分钟'})
CREATE (e_22:Exercise {id:'exercise_22', name:'五禽戏2', effect:'强筋健骨', method:'饭后1小时'})
CREATE (e_23:Exercise {id:'exercise_23', name:'易筋经2', effect:'提升免疫', method:'清晨练习'})
CREATE (e_24:Exercise {id:'exercise_24', name:'六字诀2', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_25:Exercise {id:'exercise_25', name:'站桩2', effect:'舒缓压力', method:'饭后1小时'})
CREATE (e_26:Exercise {id:'exercise_26', name:'散步2', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_27:Exercise {id:'exercise_27', name:'慢跑2', effect:'舒缓压力', method:'饭前1小时'})
CREATE (e_28:Exercise {id:'exercise_28', name:'快走2', effect:'平衡阴阳', method:'清晨练习'})
CREATE (e_29:Exercise {id:'exercise_29', name:'游泳2', effect:'增强体质', method:'每周3-5次'})
CREATE (e_30:Exercise {id:'exercise_30', name:'瑜伽2', effect:'增强体质', method:'清晨练习'})
CREATE (e_31:Exercise {id:'exercise_31', name:'普拉提2', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_32:Exercise {id:'exercise_32', name:'健身操2', effect:'舒缓压力', method:'每日1次'})
CREATE (e_33:Exercise {id:'exercise_33', name:'广场舞2', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_34:Exercise {id:'exercise_34', name:'跳绳2', effect:'调和气血', method:'每次20分钟'})
CREATE (e_35:Exercise {id:'exercise_35', name:'爬楼梯2', effect:'减肥塑形', method:'饭前1小时'})
CREATE (e_36:Exercise {id:'exercise_36', name:'骑行2', effect:'调理脏腑', method:'每周3-5次'})
CREATE (e_37:Exercise {id:'exercise_37', name:'登山2', effect:'强筋健骨', method:'每次20分钟'})
CREATE (e_38:Exercise {id:'exercise_38', name:'气功2', effect:'强筋健骨', method:'饭后1小时'})
CREATE (e_39:Exercise {id:'exercise_39', name:'导引术2', effect:'疏通经络', method:'每次45分钟'})
CREATE (e_40:Exercise {id:'exercise_40', name:'八段锦3', effect:'疏通经络', method:'每次45分钟'})
CREATE (e_41:Exercise {id:'exercise_41', name:'太极拳3', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_42:Exercise {id:'exercise_42', name:'五禽戏3', effect:'强筋健骨', method:'傍晚练习'})
CREATE (e_43:Exercise {id:'exercise_43', name:'易筋经3', effect:'增强体质', method:'清晨练习'})
CREATE (e_44:Exercise {id:'exercise_44', name:'六字诀3', effect:'调理脏腑', method:'清晨练习'})
CREATE (e_45:Exercise {id:'exercise_45', name:'站桩3', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_46:Exercise {id:'exercise_46', name:'散步3', effect:'疏通经络', method:'每日1次'})
CREATE (e_47:Exercise {id:'exercise_47', name:'慢跑3', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_48:Exercise {id:'exercise_48', name:'快走3', effect:'调和气血', method:'清晨练习'})
CREATE (e_49:Exercise {id:'exercise_49', name:'游泳3', effect:'调和气血', method:'饭前1小时'})
CREATE (e_50:Exercise {id:'exercise_50', name:'瑜伽3', effect:'舒缓压力', method:'每次45分钟'})
CREATE (e_51:Exercise {id:'exercise_51', name:'普拉提3', effect:'增强体质', method:'每次20分钟'})
CREATE (e_52:Exercise {id:'exercise_52', name:'健身操3', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_53:Exercise {id:'exercise_53', name:'广场舞3', effect:'改善睡眠', method:'清晨练习'})
CREATE (e_54:Exercise {id:'exercise_54', name:'跳绳3', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_55:Exercise {id:'exercise_55', name:'爬楼梯3', effect:'疏通经络', method:'每周3-5次'})
CREATE (e_56:Exercise {id:'exercise_56', name:'骑行3', effect:'强筋健骨', method:'每次45分钟'})
CREATE (e_57:Exercise {id:'exercise_57', name:'登山3', effect:'调和气血', method:'每周3-5次'})
CREATE (e_58:Exercise {id:'exercise_58', name:'气功3', effect:'舒缓压力', method:'饭前1小时'})
CREATE (e_59:Exercise {id:'exercise_59', name:'导引术3', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_60:Exercise {id:'exercise_60', name:'八段锦4', effect:'提升免疫', method:'每周3-5次'})
CREATE (e_61:Exercise {id:'exercise_61', name:'太极拳4', effect:'提升免疫', method:'每周3-5次'})
CREATE (e_62:Exercise {id:'exercise_62', name:'五禽戏4', effect:'调理脏腑', method:'傍晚练习'})
CREATE (e_63:Exercise {id:'exercise_63', name:'易筋经4', effect:'平衡阴阳', method:'每日1次'})
CREATE (e_64:Exercise {id:'exercise_64', name:'六字诀4', effect:'强筋健骨', method:'每日1次'})
CREATE (e_65:Exercise {id:'exercise_65', name:'站桩4', effect:'平衡阴阳', method:'每次45分钟'})
CREATE (e_66:Exercise {id:'exercise_66', name:'散步4', effect:'调和气血', method:'每次30分钟'})
CREATE (e_67:Exercise {id:'exercise_67', name:'慢跑4', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_68:Exercise {id:'exercise_68', name:'快走4', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_69:Exercise {id:'exercise_69', name:'游泳4', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_70:Exercise {id:'exercise_70', name:'瑜伽4', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_71:Exercise {id:'exercise_71', name:'普拉提4', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_72:Exercise {id:'exercise_72', name:'健身操4', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_73:Exercise {id:'exercise_73', name:'广场舞4', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_74:Exercise {id:'exercise_74', name:'跳绳4', effect:'改善睡眠', method:'饭后1小时'})
CREATE (e_75:Exercise {id:'exercise_75', name:'爬楼梯4', effect:'调理脏腑', method:'傍晚练习'})
CREATE (e_76:Exercise {id:'exercise_76', name:'骑行4', effect:'调理脏腑', method:'清晨练习'})
CREATE (e_77:Exercise {id:'exercise_77', name:'登山4', effect:'舒缓压力', method:'饭前1小时'})
CREATE (e_78:Exercise {id:'exercise_78', name:'气功4', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_79:Exercise {id:'exercise_79', name:'导引术4', effect:'改善睡眠', method:'每次30分钟'})
CREATE (e_80:Exercise {id:'exercise_80', name:'八段锦5', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_81:Exercise {id:'exercise_81', name:'太极拳5', effect:'强筋健骨', method:'傍晚练习'})
CREATE (e_82:Exercise {id:'exercise_82', name:'五禽戏5', effect:'舒缓压力', method:'傍晚练习'})
CREATE (e_83:Exercise {id:'exercise_83', name:'易筋经5', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_84:Exercise {id:'exercise_84', name:'六字诀5', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_85:Exercise {id:'exercise_85', name:'站桩5', effect:'改善睡眠', method:'每次45分钟'})
CREATE (e_86:Exercise {id:'exercise_86', name:'散步5', effect:'调理脏腑', method:'每日1次'})
CREATE (e_87:Exercise {id:'exercise_87', name:'慢跑5', effect:'增强体质', method:'傍晚练习'})
CREATE (e_88:Exercise {id:'exercise_88', name:'快走5', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_89:Exercise {id:'exercise_89', name:'游泳5', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_90:Exercise {id:'exercise_90', name:'瑜伽5', effect:'调和气血', method:'傍晚练习'})
CREATE (e_91:Exercise {id:'exercise_91', name:'普拉提5', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_92:Exercise {id:'exercise_92', name:'健身操5', effect:'提升免疫', method:'每周3-5次'})
CREATE (e_93:Exercise {id:'exercise_93', name:'广场舞5', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_94:Exercise {id:'exercise_94', name:'跳绳5', effect:'调理脏腑', method:'清晨练习'})
CREATE (e_95:Exercise {id:'exercise_95', name:'爬楼梯5', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_96:Exercise {id:'exercise_96', name:'骑行5', effect:'增强体质', method:'傍晚练习'})
CREATE (e_97:Exercise {id:'exercise_97', name:'登山5', effect:'增强体质', method:'傍晚练习'})
CREATE (e_98:Exercise {id:'exercise_98', name:'气功5', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_99:Exercise {id:'exercise_99', name:'导引术5', effect:'增强体质', method:'清晨练习'})
CREATE (e_100:Exercise {id:'exercise_100', name:'八段锦6', effect:'平衡阴阳', method:'每周3-5次'})
CREATE (e_101:Exercise {id:'exercise_101', name:'太极拳6', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_102:Exercise {id:'exercise_102', name:'五禽戏6', effect:'疏通经络', method:'每周3-5次'})
CREATE (e_103:Exercise {id:'exercise_103', name:'易筋经6', effect:'提升免疫', method:'每周3-5次'})
CREATE (e_104:Exercise {id:'exercise_104', name:'六字诀6', effect:'强筋健骨', method:'傍晚练习'})
CREATE (e_105:Exercise {id:'exercise_105', name:'站桩6', effect:'疏通经络', method:'清晨练习'})
CREATE (e_106:Exercise {id:'exercise_106', name:'散步6', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_107:Exercise {id:'exercise_107', name:'慢跑6', effect:'增强体质', method:'每日1次'})
CREATE (e_108:Exercise {id:'exercise_108', name:'快走6', effect:'增强体质', method:'每次20分钟'})
CREATE (e_109:Exercise {id:'exercise_109', name:'游泳6', effect:'增强体质', method:'饭前1小时'})
CREATE (e_110:Exercise {id:'exercise_110', name:'瑜伽6', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_111:Exercise {id:'exercise_111', name:'普拉提6', effect:'减肥塑形', method:'傍晚练习'})
CREATE (e_112:Exercise {id:'exercise_112', name:'健身操6', effect:'增强体质', method:'清晨练习'})
CREATE (e_113:Exercise {id:'exercise_113', name:'广场舞6', effect:'调和气血', method:'饭后1小时'})
CREATE (e_114:Exercise {id:'exercise_114', name:'跳绳6', effect:'调和气血', method:'傍晚练习'})
CREATE (e_115:Exercise {id:'exercise_115', name:'爬楼梯6', effect:'舒缓压力', method:'每日1次'})
CREATE (e_116:Exercise {id:'exercise_116', name:'骑行6', effect:'减肥塑形', method:'傍晚练习'})
CREATE (e_117:Exercise {id:'exercise_117', name:'登山6', effect:'强筋健骨', method:'饭后1小时'})
CREATE (e_118:Exercise {id:'exercise_118', name:'气功6', effect:'改善睡眠', method:'每日1次'})
CREATE (e_119:Exercise {id:'exercise_119', name:'导引术6', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_120:Exercise {id:'exercise_120', name:'八段锦7', effect:'平衡阴阳', method:'傍晚练习'})
CREATE (e_121:Exercise {id:'exercise_121', name:'太极拳7', effect:'减肥塑形', method:'每周3-5次'})
CREATE (e_122:Exercise {id:'exercise_122', name:'五禽戏7', effect:'舒缓压力', method:'每日1次'})
CREATE (e_123:Exercise {id:'exercise_123', name:'易筋经7', effect:'改善睡眠', method:'清晨练习'})
CREATE (e_124:Exercise {id:'exercise_124', name:'六字诀7', effect:'提升免疫', method:'每日1次'})
CREATE (e_125:Exercise {id:'exercise_125', name:'站桩7', effect:'增强体质', method:'每次30分钟'})
CREATE (e_126:Exercise {id:'exercise_126', name:'散步7', effect:'调和气血', method:'每周3-5次'})
CREATE (e_127:Exercise {id:'exercise_127', name:'慢跑7', effect:'改善睡眠', method:'饭后1小时'})
CREATE (e_128:Exercise {id:'exercise_128', name:'快走7', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_129:Exercise {id:'exercise_129', name:'游泳7', effect:'增强体质', method:'清晨练习'})
CREATE (e_130:Exercise {id:'exercise_130', name:'瑜伽7', effect:'增强体质', method:'清晨练习'})
CREATE (e_131:Exercise {id:'exercise_131', name:'普拉提7', effect:'增强体质', method:'清晨练习'})
CREATE (e_132:Exercise {id:'exercise_132', name:'健身操7', effect:'平衡阴阳', method:'每次45分钟'})
CREATE (e_133:Exercise {id:'exercise_133', name:'广场舞7', effect:'舒缓压力', method:'饭前1小时'})
CREATE (e_134:Exercise {id:'exercise_134', name:'跳绳7', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_135:Exercise {id:'exercise_135', name:'爬楼梯7', effect:'增强体质', method:'每次45分钟'})
CREATE (e_136:Exercise {id:'exercise_136', name:'骑行7', effect:'增强体质', method:'傍晚练习'})
CREATE (e_137:Exercise {id:'exercise_137', name:'登山7', effect:'调理脏腑', method:'每次45分钟'})
CREATE (e_138:Exercise {id:'exercise_138', name:'气功7', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_139:Exercise {id:'exercise_139', name:'导引术7', effect:'提升免疫', method:'每周3-5次'})
CREATE (e_140:Exercise {id:'exercise_140', name:'八段锦8', effect:'疏通经络', method:'每次45分钟'})
CREATE (e_141:Exercise {id:'exercise_141', name:'太极拳8', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_142:Exercise {id:'exercise_142', name:'五禽戏8', effect:'减肥塑形', method:'饭前1小时'})
CREATE (e_143:Exercise {id:'exercise_143', name:'易筋经8', effect:'平衡阴阳', method:'每日1次'})
CREATE (e_144:Exercise {id:'exercise_144', name:'六字诀8', effect:'调和气血', method:'每日1次'})
CREATE (e_145:Exercise {id:'exercise_145', name:'站桩8', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_146:Exercise {id:'exercise_146', name:'散步8', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_147:Exercise {id:'exercise_147', name:'慢跑8', effect:'疏通经络', method:'每日1次'})
CREATE (e_148:Exercise {id:'exercise_148', name:'快走8', effect:'舒缓压力', method:'饭前1小时'})
CREATE (e_149:Exercise {id:'exercise_149', name:'游泳8', effect:'疏通经络', method:'每次45分钟'})
CREATE (e_150:Exercise {id:'exercise_150', name:'瑜伽8', effect:'调理脏腑', method:'每日1次'})
CREATE (e_151:Exercise {id:'exercise_151', name:'普拉提8', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_152:Exercise {id:'exercise_152', name:'健身操8', effect:'提升免疫', method:'清晨练习'})
CREATE (e_153:Exercise {id:'exercise_153', name:'广场舞8', effect:'改善睡眠', method:'每日1次'})
CREATE (e_154:Exercise {id:'exercise_154', name:'跳绳8', effect:'调理脏腑', method:'每日1次'})
CREATE (e_155:Exercise {id:'exercise_155', name:'爬楼梯8', effect:'提升免疫', method:'清晨练习'})
CREATE (e_156:Exercise {id:'exercise_156', name:'骑行8', effect:'调理脏腑', method:'傍晚练习'})
CREATE (e_157:Exercise {id:'exercise_157', name:'登山8', effect:'增强体质', method:'每次30分钟'})
CREATE (e_158:Exercise {id:'exercise_158', name:'气功8', effect:'舒缓压力', method:'傍晚练习'})
CREATE (e_159:Exercise {id:'exercise_159', name:'导引术8', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_160:Exercise {id:'exercise_160', name:'八段锦9', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_161:Exercise {id:'exercise_161', name:'太极拳9', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_162:Exercise {id:'exercise_162', name:'五禽戏9', effect:'调和气血', method:'每次20分钟'})
CREATE (e_163:Exercise {id:'exercise_163', name:'易筋经9', effect:'平衡阴阳', method:'每次45分钟'})
CREATE (e_164:Exercise {id:'exercise_164', name:'六字诀9', effect:'增强体质', method:'每周3-5次'})
CREATE (e_165:Exercise {id:'exercise_165', name:'站桩9', effect:'疏通经络', method:'清晨练习'})
CREATE (e_166:Exercise {id:'exercise_166', name:'散步9', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_167:Exercise {id:'exercise_167', name:'慢跑9', effect:'调理脏腑', method:'每次30分钟'})
CREATE (e_168:Exercise {id:'exercise_168', name:'快走9', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_169:Exercise {id:'exercise_169', name:'游泳9', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_170:Exercise {id:'exercise_170', name:'瑜伽9', effect:'改善睡眠', method:'饭前1小时'})
CREATE (e_171:Exercise {id:'exercise_171', name:'普拉提9', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_172:Exercise {id:'exercise_172', name:'健身操9', effect:'疏通经络', method:'每次30分钟'})
CREATE (e_173:Exercise {id:'exercise_173', name:'广场舞9', effect:'舒缓压力', method:'饭后1小时'})
CREATE (e_174:Exercise {id:'exercise_174', name:'跳绳9', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_175:Exercise {id:'exercise_175', name:'爬楼梯9', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_176:Exercise {id:'exercise_176', name:'骑行9', effect:'调理脏腑', method:'每日1次'})
CREATE (e_177:Exercise {id:'exercise_177', name:'登山9', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_178:Exercise {id:'exercise_178', name:'气功9', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_179:Exercise {id:'exercise_179', name:'导引术9', effect:'增强体质', method:'清晨练习'})
CREATE (e_180:Exercise {id:'exercise_180', name:'八段锦10', effect:'强筋健骨', method:'清晨练习'})
CREATE (e_181:Exercise {id:'exercise_181', name:'太极拳10', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_182:Exercise {id:'exercise_182', name:'五禽戏10', effect:'减肥塑形', method:'清晨练习'})
CREATE (e_183:Exercise {id:'exercise_183', name:'易筋经10', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_184:Exercise {id:'exercise_184', name:'六字诀10', effect:'强筋健骨', method:'每次20分钟'})
CREATE (e_185:Exercise {id:'exercise_185', name:'站桩10', effect:'改善睡眠', method:'每次20分钟'})
CREATE (e_186:Exercise {id:'exercise_186', name:'散步10', effect:'强筋健骨', method:'饭后1小时'})
CREATE (e_187:Exercise {id:'exercise_187', name:'慢跑10', effect:'强筋健骨', method:'每日1次'})
CREATE (e_188:Exercise {id:'exercise_188', name:'快走10', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_189:Exercise {id:'exercise_189', name:'游泳10', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_190:Exercise {id:'exercise_190', name:'瑜伽10', effect:'平衡阴阳', method:'每周3-5次'})
CREATE (e_191:Exercise {id:'exercise_191', name:'普拉提10', effect:'增强体质', method:'每次20分钟'})
CREATE (e_192:Exercise {id:'exercise_192', name:'健身操10', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_193:Exercise {id:'exercise_193', name:'广场舞10', effect:'调理脏腑', method:'傍晚练习'})
CREATE (e_194:Exercise {id:'exercise_194', name:'跳绳10', effect:'减肥塑形', method:'清晨练习'})
CREATE (e_195:Exercise {id:'exercise_195', name:'爬楼梯10', effect:'增强体质', method:'每次20分钟'})
CREATE (e_196:Exercise {id:'exercise_196', name:'骑行10', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_197:Exercise {id:'exercise_197', name:'登山10', effect:'疏通经络', method:'每次45分钟'})
CREATE (e_198:Exercise {id:'exercise_198', name:'气功10', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_199:Exercise {id:'exercise_199', name:'导引术10', effect:'增强体质', method:'傍晚练习'})
CREATE (e_200:Exercise {id:'exercise_200', name:'八段锦11', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_201:Exercise {id:'exercise_201', name:'太极拳11', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_202:Exercise {id:'exercise_202', name:'五禽戏11', effect:'减肥塑形', method:'傍晚练习'})
CREATE (e_203:Exercise {id:'exercise_203', name:'易筋经11', effect:'改善睡眠', method:'每次30分钟'})
CREATE (e_204:Exercise {id:'exercise_204', name:'六字诀11', effect:'提升免疫', method:'每日1次'})
CREATE (e_205:Exercise {id:'exercise_205', name:'站桩11', effect:'疏通经络', method:'每周3-5次'})
CREATE (e_206:Exercise {id:'exercise_206', name:'散步11', effect:'平衡阴阳', method:'每次45分钟'})
CREATE (e_207:Exercise {id:'exercise_207', name:'慢跑11', effect:'平衡阴阳', method:'饭后1小时'})
CREATE (e_208:Exercise {id:'exercise_208', name:'快走11', effect:'减肥塑形', method:'饭前1小时'})
CREATE (e_209:Exercise {id:'exercise_209', name:'游泳11', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_210:Exercise {id:'exercise_210', name:'瑜伽11', effect:'平衡阴阳', method:'饭后1小时'})
CREATE (e_211:Exercise {id:'exercise_211', name:'普拉提11', effect:'疏通经络', method:'饭后1小时'})
CREATE (e_212:Exercise {id:'exercise_212', name:'健身操11', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_213:Exercise {id:'exercise_213', name:'广场舞11', effect:'减肥塑形', method:'傍晚练习'})
CREATE (e_214:Exercise {id:'exercise_214', name:'跳绳11', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_215:Exercise {id:'exercise_215', name:'爬楼梯11', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_216:Exercise {id:'exercise_216', name:'骑行11', effect:'增强体质', method:'傍晚练习'})
CREATE (e_217:Exercise {id:'exercise_217', name:'登山11', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_218:Exercise {id:'exercise_218', name:'气功11', effect:'疏通经络', method:'饭后1小时'})
CREATE (e_219:Exercise {id:'exercise_219', name:'导引术11', effect:'调和气血', method:'清晨练习'})
CREATE (e_220:Exercise {id:'exercise_220', name:'八段锦12', effect:'强筋健骨', method:'傍晚练习'})
CREATE (e_221:Exercise {id:'exercise_221', name:'太极拳12', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_222:Exercise {id:'exercise_222', name:'五禽戏12', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_223:Exercise {id:'exercise_223', name:'易筋经12', effect:'调和气血', method:'每次30分钟'})
CREATE (e_224:Exercise {id:'exercise_224', name:'六字诀12', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_225:Exercise {id:'exercise_225', name:'站桩12', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_226:Exercise {id:'exercise_226', name:'散步12', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_227:Exercise {id:'exercise_227', name:'慢跑12', effect:'减肥塑形', method:'饭前1小时'})
CREATE (e_228:Exercise {id:'exercise_228', name:'快走12', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_229:Exercise {id:'exercise_229', name:'游泳12', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_230:Exercise {id:'exercise_230', name:'瑜伽12', effect:'增强体质', method:'饭前1小时'})
CREATE (e_231:Exercise {id:'exercise_231', name:'普拉提12', effect:'调和气血', method:'每次30分钟'})
CREATE (e_232:Exercise {id:'exercise_232', name:'健身操12', effect:'调理脏腑', method:'清晨练习'})
CREATE (e_233:Exercise {id:'exercise_233', name:'广场舞12', effect:'调理脏腑', method:'每日1次'})
CREATE (e_234:Exercise {id:'exercise_234', name:'跳绳12', effect:'减肥塑形', method:'饭前1小时'})
CREATE (e_235:Exercise {id:'exercise_235', name:'爬楼梯12', effect:'调和气血', method:'每周3-5次'})
CREATE (e_236:Exercise {id:'exercise_236', name:'骑行12', effect:'减肥塑形', method:'每日1次'})
CREATE (e_237:Exercise {id:'exercise_237', name:'登山12', effect:'调和气血', method:'饭后1小时'})
CREATE (e_238:Exercise {id:'exercise_238', name:'气功12', effect:'平衡阴阳', method:'每日1次'})
CREATE (e_239:Exercise {id:'exercise_239', name:'导引术12', effect:'改善睡眠', method:'饭前1小时'})
CREATE (e_240:Exercise {id:'exercise_240', name:'八段锦13', effect:'调理脏腑', method:'清晨练习'})
CREATE (e_241:Exercise {id:'exercise_241', name:'太极拳13', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_242:Exercise {id:'exercise_242', name:'五禽戏13', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_243:Exercise {id:'exercise_243', name:'易筋经13', effect:'增强体质', method:'每日1次'})
CREATE (e_244:Exercise {id:'exercise_244', name:'六字诀13', effect:'强筋健骨', method:'每周3-5次'})
CREATE (e_245:Exercise {id:'exercise_245', name:'站桩13', effect:'改善睡眠', method:'每次30分钟'})
CREATE (e_246:Exercise {id:'exercise_246', name:'散步13', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_247:Exercise {id:'exercise_247', name:'慢跑13', effect:'强筋健骨', method:'每次20分钟'})
CREATE (e_248:Exercise {id:'exercise_248', name:'快走13', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_249:Exercise {id:'exercise_249', name:'游泳13', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_250:Exercise {id:'exercise_250', name:'瑜伽13', effect:'改善睡眠', method:'每日1次'})
CREATE (e_251:Exercise {id:'exercise_251', name:'普拉提13', effect:'增强体质', method:'清晨练习'})
CREATE (e_252:Exercise {id:'exercise_252', name:'健身操13', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_253:Exercise {id:'exercise_253', name:'广场舞13', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_254:Exercise {id:'exercise_254', name:'跳绳13', effect:'强筋健骨', method:'每日1次'})
CREATE (e_255:Exercise {id:'exercise_255', name:'爬楼梯13', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_256:Exercise {id:'exercise_256', name:'骑行13', effect:'疏通经络', method:'清晨练习'})
CREATE (e_257:Exercise {id:'exercise_257', name:'登山13', effect:'强筋健骨', method:'傍晚练习'})
CREATE (e_258:Exercise {id:'exercise_258', name:'气功13', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_259:Exercise {id:'exercise_259', name:'导引术13', effect:'增强体质', method:'饭后1小时'})
CREATE (e_260:Exercise {id:'exercise_260', name:'八段锦14', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_261:Exercise {id:'exercise_261', name:'太极拳14', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_262:Exercise {id:'exercise_262', name:'五禽戏14', effect:'改善睡眠', method:'清晨练习'})
CREATE (e_263:Exercise {id:'exercise_263', name:'易筋经14', effect:'增强体质', method:'每日1次'})
CREATE (e_264:Exercise {id:'exercise_264', name:'六字诀14', effect:'调理脏腑', method:'每次45分钟'})
CREATE (e_265:Exercise {id:'exercise_265', name:'站桩14', effect:'增强体质', method:'每日1次'})
CREATE (e_266:Exercise {id:'exercise_266', name:'散步14', effect:'疏通经络', method:'每次45分钟'})
CREATE (e_267:Exercise {id:'exercise_267', name:'慢跑14', effect:'强筋健骨', method:'傍晚练习'})
CREATE (e_268:Exercise {id:'exercise_268', name:'快走14', effect:'强筋健骨', method:'清晨练习'})
CREATE (e_269:Exercise {id:'exercise_269', name:'游泳14', effect:'平衡阴阳', method:'每周3-5次'})
CREATE (e_270:Exercise {id:'exercise_270', name:'瑜伽14', effect:'疏通经络', method:'傍晚练习'})
CREATE (e_271:Exercise {id:'exercise_271', name:'普拉提14', effect:'改善睡眠', method:'清晨练习'})
CREATE (e_272:Exercise {id:'exercise_272', name:'健身操14', effect:'减肥塑形', method:'每周3-5次'})
CREATE (e_273:Exercise {id:'exercise_273', name:'广场舞14', effect:'疏通经络', method:'每次45分钟'})
CREATE (e_274:Exercise {id:'exercise_274', name:'跳绳14', effect:'改善睡眠', method:'每日1次'})
CREATE (e_275:Exercise {id:'exercise_275', name:'爬楼梯14', effect:'减肥塑形', method:'傍晚练习'})
CREATE (e_276:Exercise {id:'exercise_276', name:'骑行14', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_277:Exercise {id:'exercise_277', name:'登山14', effect:'增强体质', method:'饭后1小时'})
CREATE (e_278:Exercise {id:'exercise_278', name:'气功14', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_279:Exercise {id:'exercise_279', name:'导引术14', effect:'舒缓压力', method:'每次20分钟'})
CREATE (e_280:Exercise {id:'exercise_280', name:'八段锦15', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_281:Exercise {id:'exercise_281', name:'太极拳15', effect:'调理脏腑', method:'每日1次'})
CREATE (e_282:Exercise {id:'exercise_282', name:'五禽戏15', effect:'调和气血', method:'每日1次'})
CREATE (e_283:Exercise {id:'exercise_283', name:'易筋经15', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_284:Exercise {id:'exercise_284', name:'六字诀15', effect:'平衡阴阳', method:'清晨练习'})
CREATE (e_285:Exercise {id:'exercise_285', name:'站桩15', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_286:Exercise {id:'exercise_286', name:'散步15', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_287:Exercise {id:'exercise_287', name:'慢跑15', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_288:Exercise {id:'exercise_288', name:'快走15', effect:'减肥塑形', method:'饭前1小时'})
CREATE (e_289:Exercise {id:'exercise_289', name:'游泳15', effect:'提升免疫', method:'饭后1小时'})
CREATE (e_290:Exercise {id:'exercise_290', name:'瑜伽15', effect:'调和气血', method:'饭前1小时'})
CREATE (e_291:Exercise {id:'exercise_291', name:'普拉提15', effect:'增强体质', method:'饭前1小时'})
CREATE (e_292:Exercise {id:'exercise_292', name:'健身操15', effect:'调理脏腑', method:'饭后1小时'})
CREATE (e_293:Exercise {id:'exercise_293', name:'广场舞15', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_294:Exercise {id:'exercise_294', name:'跳绳15', effect:'减肥塑形', method:'每日1次'})
CREATE (e_295:Exercise {id:'exercise_295', name:'爬楼梯15', effect:'调和气血', method:'每次45分钟'})
CREATE (e_296:Exercise {id:'exercise_296', name:'骑行15', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_297:Exercise {id:'exercise_297', name:'登山15', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_298:Exercise {id:'exercise_298', name:'气功15', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_299:Exercise {id:'exercise_299', name:'导引术15', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_300:Exercise {id:'exercise_300', name:'八段锦16', effect:'疏通经络', method:'饭前1小时'})
CREATE (e_301:Exercise {id:'exercise_301', name:'太极拳16', effect:'增强体质', method:'每日1次'})
CREATE (e_302:Exercise {id:'exercise_302', name:'五禽戏16', effect:'调理脏腑', method:'饭后1小时'})
CREATE (e_303:Exercise {id:'exercise_303', name:'易筋经16', effect:'提升免疫', method:'清晨练习'})
CREATE (e_304:Exercise {id:'exercise_304', name:'六字诀16', effect:'平衡阴阳', method:'每日1次'})
CREATE (e_305:Exercise {id:'exercise_305', name:'站桩16', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_306:Exercise {id:'exercise_306', name:'散步16', effect:'平衡阴阳', method:'每次30分钟'})
CREATE (e_307:Exercise {id:'exercise_307', name:'慢跑16', effect:'调理脏腑', method:'每日1次'})
CREATE (e_308:Exercise {id:'exercise_308', name:'快走16', effect:'强筋健骨', method:'每日1次'})
CREATE (e_309:Exercise {id:'exercise_309', name:'游泳16', effect:'强筋健骨', method:'每日1次'})
CREATE (e_310:Exercise {id:'exercise_310', name:'瑜伽16', effect:'调和气血', method:'清晨练习'})
CREATE (e_311:Exercise {id:'exercise_311', name:'普拉提16', effect:'疏通经络', method:'清晨练习'})
CREATE (e_312:Exercise {id:'exercise_312', name:'健身操16', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_313:Exercise {id:'exercise_313', name:'广场舞16', effect:'调和气血', method:'清晨练习'})
CREATE (e_314:Exercise {id:'exercise_314', name:'跳绳16', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_315:Exercise {id:'exercise_315', name:'爬楼梯16', effect:'平衡阴阳', method:'每日1次'})
CREATE (e_316:Exercise {id:'exercise_316', name:'骑行16', effect:'调和气血', method:'每次30分钟'})
CREATE (e_317:Exercise {id:'exercise_317', name:'登山16', effect:'改善睡眠', method:'饭后1小时'})
CREATE (e_318:Exercise {id:'exercise_318', name:'气功16', effect:'增强体质', method:'每周3-5次'})
CREATE (e_319:Exercise {id:'exercise_319', name:'导引术16', effect:'调和气血', method:'饭后1小时'})
CREATE (e_320:Exercise {id:'exercise_320', name:'八段锦17', effect:'调和气血', method:'每次45分钟'})
CREATE (e_321:Exercise {id:'exercise_321', name:'太极拳17', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_322:Exercise {id:'exercise_322', name:'五禽戏17', effect:'强筋健骨', method:'清晨练习'})
CREATE (e_323:Exercise {id:'exercise_323', name:'易筋经17', effect:'平衡阴阳', method:'饭后1小时'})
CREATE (e_324:Exercise {id:'exercise_324', name:'六字诀17', effect:'疏通经络', method:'饭前1小时'})
CREATE (e_325:Exercise {id:'exercise_325', name:'站桩17', effect:'改善睡眠', method:'每次45分钟'})
CREATE (e_326:Exercise {id:'exercise_326', name:'散步17', effect:'调和气血', method:'每次45分钟'})
CREATE (e_327:Exercise {id:'exercise_327', name:'慢跑17', effect:'提升免疫', method:'每日1次'})
CREATE (e_328:Exercise {id:'exercise_328', name:'快走17', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_329:Exercise {id:'exercise_329', name:'游泳17', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_330:Exercise {id:'exercise_330', name:'瑜伽17', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_331:Exercise {id:'exercise_331', name:'普拉提17', effect:'提升免疫', method:'饭前1小时'})
CREATE (e_332:Exercise {id:'exercise_332', name:'健身操17', effect:'舒缓压力', method:'饭后1小时'})
CREATE (e_333:Exercise {id:'exercise_333', name:'广场舞17', effect:'改善睡眠', method:'每次20分钟'})
CREATE (e_334:Exercise {id:'exercise_334', name:'跳绳17', effect:'强筋健骨', method:'傍晚练习'})
CREATE (e_335:Exercise {id:'exercise_335', name:'爬楼梯17', effect:'提升免疫', method:'饭前1小时'})
CREATE (e_336:Exercise {id:'exercise_336', name:'骑行17', effect:'疏通经络', method:'清晨练习'})
CREATE (e_337:Exercise {id:'exercise_337', name:'登山17', effect:'提升免疫', method:'清晨练习'})
CREATE (e_338:Exercise {id:'exercise_338', name:'气功17', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_339:Exercise {id:'exercise_339', name:'导引术17', effect:'增强体质', method:'清晨练习'})
CREATE (e_340:Exercise {id:'exercise_340', name:'八段锦18', effect:'增强体质', method:'清晨练习'})
CREATE (e_341:Exercise {id:'exercise_341', name:'太极拳18', effect:'改善睡眠', method:'每周3-5次'})
CREATE (e_342:Exercise {id:'exercise_342', name:'五禽戏18', effect:'减肥塑形', method:'清晨练习'})
CREATE (e_343:Exercise {id:'exercise_343', name:'易筋经18', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_344:Exercise {id:'exercise_344', name:'六字诀18', effect:'调和气血', method:'每日1次'})
CREATE (e_345:Exercise {id:'exercise_345', name:'站桩18', effect:'强筋健骨', method:'每周3-5次'})
CREATE (e_346:Exercise {id:'exercise_346', name:'散步18', effect:'舒缓压力', method:'饭后1小时'})
CREATE (e_347:Exercise {id:'exercise_347', name:'慢跑18', effect:'调理脏腑', method:'每次30分钟'})
CREATE (e_348:Exercise {id:'exercise_348', name:'快走18', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_349:Exercise {id:'exercise_349', name:'游泳18', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_350:Exercise {id:'exercise_350', name:'瑜伽18', effect:'增强体质', method:'清晨练习'})
CREATE (e_351:Exercise {id:'exercise_351', name:'普拉提18', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_352:Exercise {id:'exercise_352', name:'健身操18', effect:'疏通经络', method:'每周3-5次'})
CREATE (e_353:Exercise {id:'exercise_353', name:'广场舞18', effect:'调理脏腑', method:'每次30分钟'})
CREATE (e_354:Exercise {id:'exercise_354', name:'跳绳18', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_355:Exercise {id:'exercise_355', name:'爬楼梯18', effect:'调和气血', method:'饭后1小时'})
CREATE (e_356:Exercise {id:'exercise_356', name:'骑行18', effect:'调理脏腑', method:'饭后1小时'})
CREATE (e_357:Exercise {id:'exercise_357', name:'登山18', effect:'疏通经络', method:'饭前1小时'})
CREATE (e_358:Exercise {id:'exercise_358', name:'气功18', effect:'改善睡眠', method:'饭前1小时'})
CREATE (e_359:Exercise {id:'exercise_359', name:'导引术18', effect:'调和气血', method:'每次30分钟'})
CREATE (e_360:Exercise {id:'exercise_360', name:'八段锦19', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_361:Exercise {id:'exercise_361', name:'太极拳19', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_362:Exercise {id:'exercise_362', name:'五禽戏19', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_363:Exercise {id:'exercise_363', name:'易筋经19', effect:'舒缓压力', method:'饭前1小时'})
CREATE (e_364:Exercise {id:'exercise_364', name:'六字诀19', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_365:Exercise {id:'exercise_365', name:'站桩19', effect:'疏通经络', method:'傍晚练习'})
CREATE (e_366:Exercise {id:'exercise_366', name:'散步19', effect:'调和气血', method:'傍晚练习'})
CREATE (e_367:Exercise {id:'exercise_367', name:'慢跑19', effect:'改善睡眠', method:'每次30分钟'})
CREATE (e_368:Exercise {id:'exercise_368', name:'快走19', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_369:Exercise {id:'exercise_369', name:'游泳19', effect:'强筋健骨', method:'每次45分钟'})
CREATE (e_370:Exercise {id:'exercise_370', name:'瑜伽19', effect:'疏通经络', method:'饭前1小时'})
CREATE (e_371:Exercise {id:'exercise_371', name:'普拉提19', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_372:Exercise {id:'exercise_372', name:'健身操19', effect:'疏通经络', method:'每周3-5次'})
CREATE (e_373:Exercise {id:'exercise_373', name:'广场舞19', effect:'提升免疫', method:'每次20分钟'})
CREATE (e_374:Exercise {id:'exercise_374', name:'跳绳19', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_375:Exercise {id:'exercise_375', name:'爬楼梯19', effect:'减肥塑形', method:'饭前1小时'})
CREATE (e_376:Exercise {id:'exercise_376', name:'骑行19', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_377:Exercise {id:'exercise_377', name:'登山19', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_378:Exercise {id:'exercise_378', name:'气功19', effect:'改善睡眠', method:'每次30分钟'})
CREATE (e_379:Exercise {id:'exercise_379', name:'导引术19', effect:'改善睡眠', method:'饭前1小时'})
CREATE (e_380:Exercise {id:'exercise_380', name:'八段锦20', effect:'强筋健骨', method:'清晨练习'})
CREATE (e_381:Exercise {id:'exercise_381', name:'太极拳20', effect:'调理脏腑', method:'每周3-5次'})
CREATE (e_382:Exercise {id:'exercise_382', name:'五禽戏20', effect:'疏通经络', method:'清晨练习'})
CREATE (e_383:Exercise {id:'exercise_383', name:'易筋经20', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_384:Exercise {id:'exercise_384', name:'六字诀20', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_385:Exercise {id:'exercise_385', name:'站桩20', effect:'减肥塑形', method:'每日1次'})
CREATE (e_386:Exercise {id:'exercise_386', name:'散步20', effect:'减肥塑形', method:'每次45分钟'})
CREATE (e_387:Exercise {id:'exercise_387', name:'慢跑20', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_388:Exercise {id:'exercise_388', name:'快走20', effect:'增强体质', method:'傍晚练习'})
CREATE (e_389:Exercise {id:'exercise_389', name:'游泳20', effect:'增强体质', method:'每周3-5次'})
CREATE (e_390:Exercise {id:'exercise_390', name:'瑜伽20', effect:'强筋健骨', method:'每次20分钟'})
CREATE (e_391:Exercise {id:'exercise_391', name:'普拉提20', effect:'舒缓压力', method:'每次20分钟'})
CREATE (e_392:Exercise {id:'exercise_392', name:'健身操20', effect:'改善睡眠', method:'饭后1小时'})
CREATE (e_393:Exercise {id:'exercise_393', name:'广场舞20', effect:'调理脏腑', method:'每次45分钟'})
CREATE (e_394:Exercise {id:'exercise_394', name:'跳绳20', effect:'增强体质', method:'饭前1小时'})
CREATE (e_395:Exercise {id:'exercise_395', name:'爬楼梯20', effect:'提升免疫', method:'每日1次'})
CREATE (e_396:Exercise {id:'exercise_396', name:'骑行20', effect:'增强体质', method:'清晨练习'})
CREATE (e_397:Exercise {id:'exercise_397', name:'登山20', effect:'平衡阴阳', method:'每日1次'})
CREATE (e_398:Exercise {id:'exercise_398', name:'气功20', effect:'改善睡眠', method:'清晨练习'})
CREATE (e_399:Exercise {id:'exercise_399', name:'导引术20', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_400:Exercise {id:'exercise_400', name:'八段锦21', effect:'调理脏腑', method:'傍晚练习'})
CREATE (e_401:Exercise {id:'exercise_401', name:'太极拳21', effect:'减肥塑形', method:'每周3-5次'})
CREATE (e_402:Exercise {id:'exercise_402', name:'五禽戏21', effect:'调理脏腑', method:'傍晚练习'})
CREATE (e_403:Exercise {id:'exercise_403', name:'易筋经21', effect:'调和气血', method:'每次30分钟'})
CREATE (e_404:Exercise {id:'exercise_404', name:'六字诀21', effect:'调和气血', method:'清晨练习'})
CREATE (e_405:Exercise {id:'exercise_405', name:'站桩21', effect:'增强体质', method:'每次45分钟'})
CREATE (e_406:Exercise {id:'exercise_406', name:'散步21', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_407:Exercise {id:'exercise_407', name:'慢跑21', effect:'强筋健骨', method:'饭后1小时'})
CREATE (e_408:Exercise {id:'exercise_408', name:'快走21', effect:'增强体质', method:'清晨练习'})
CREATE (e_409:Exercise {id:'exercise_409', name:'游泳21', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_410:Exercise {id:'exercise_410', name:'瑜伽21', effect:'增强体质', method:'每次30分钟'})
CREATE (e_411:Exercise {id:'exercise_411', name:'普拉提21', effect:'增强体质', method:'每次20分钟'})
CREATE (e_412:Exercise {id:'exercise_412', name:'健身操21', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_413:Exercise {id:'exercise_413', name:'广场舞21', effect:'改善睡眠', method:'饭前1小时'})
CREATE (e_414:Exercise {id:'exercise_414', name:'跳绳21', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_415:Exercise {id:'exercise_415', name:'爬楼梯21', effect:'提升免疫', method:'傍晚练习'})
CREATE (e_416:Exercise {id:'exercise_416', name:'骑行21', effect:'调理脏腑', method:'每次45分钟'})
CREATE (e_417:Exercise {id:'exercise_417', name:'登山21', effect:'调理脏腑', method:'每周3-5次'})
CREATE (e_418:Exercise {id:'exercise_418', name:'气功21', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_419:Exercise {id:'exercise_419', name:'导引术21', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_420:Exercise {id:'exercise_420', name:'八段锦22', effect:'调理脏腑', method:'傍晚练习'})
CREATE (e_421:Exercise {id:'exercise_421', name:'太极拳22', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_422:Exercise {id:'exercise_422', name:'五禽戏22', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_423:Exercise {id:'exercise_423', name:'易筋经22', effect:'调和气血', method:'每次20分钟'})
CREATE (e_424:Exercise {id:'exercise_424', name:'六字诀22', effect:'舒缓压力', method:'清晨练习'})
CREATE (e_425:Exercise {id:'exercise_425', name:'站桩22', effect:'调理脏腑', method:'每次30分钟'})
CREATE (e_426:Exercise {id:'exercise_426', name:'散步22', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_427:Exercise {id:'exercise_427', name:'慢跑22', effect:'增强体质', method:'每次45分钟'})
CREATE (e_428:Exercise {id:'exercise_428', name:'快走22', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_429:Exercise {id:'exercise_429', name:'游泳22', effect:'舒缓压力', method:'每日1次'})
CREATE (e_430:Exercise {id:'exercise_430', name:'瑜伽22', effect:'舒缓压力', method:'饭后1小时'})
CREATE (e_431:Exercise {id:'exercise_431', name:'普拉提22', effect:'疏通经络', method:'每次20分钟'})
CREATE (e_432:Exercise {id:'exercise_432', name:'健身操22', effect:'增强体质', method:'每周3-5次'})
CREATE (e_433:Exercise {id:'exercise_433', name:'广场舞22', effect:'舒缓压力', method:'每次30分钟'})
CREATE (e_434:Exercise {id:'exercise_434', name:'跳绳22', effect:'减肥塑形', method:'清晨练习'})
CREATE (e_435:Exercise {id:'exercise_435', name:'爬楼梯22', effect:'平衡阴阳', method:'每次45分钟'})
CREATE (e_436:Exercise {id:'exercise_436', name:'骑行22', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_437:Exercise {id:'exercise_437', name:'登山22', effect:'增强体质', method:'傍晚练习'})
CREATE (e_438:Exercise {id:'exercise_438', name:'气功22', effect:'提升免疫', method:'清晨练习'})
CREATE (e_439:Exercise {id:'exercise_439', name:'导引术22', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_440:Exercise {id:'exercise_440', name:'八段锦23', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_441:Exercise {id:'exercise_441', name:'太极拳23', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_442:Exercise {id:'exercise_442', name:'五禽戏23', effect:'增强体质', method:'每次20分钟'})
CREATE (e_443:Exercise {id:'exercise_443', name:'易筋经23', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_444:Exercise {id:'exercise_444', name:'六字诀23', effect:'调和气血', method:'傍晚练习'})
CREATE (e_445:Exercise {id:'exercise_445', name:'站桩23', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_446:Exercise {id:'exercise_446', name:'散步23', effect:'调和气血', method:'饭后1小时'})
CREATE (e_447:Exercise {id:'exercise_447', name:'慢跑23', effect:'疏通经络', method:'饭前1小时'})
CREATE (e_448:Exercise {id:'exercise_448', name:'快走23', effect:'疏通经络', method:'傍晚练习'})
CREATE (e_449:Exercise {id:'exercise_449', name:'游泳23', effect:'舒缓压力', method:'饭前1小时'})
CREATE (e_450:Exercise {id:'exercise_450', name:'瑜伽23', effect:'改善睡眠', method:'每次20分钟'})
CREATE (e_451:Exercise {id:'exercise_451', name:'普拉提23', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_452:Exercise {id:'exercise_452', name:'健身操23', effect:'强筋健骨', method:'每日1次'})
CREATE (e_453:Exercise {id:'exercise_453', name:'广场舞23', effect:'调理脏腑', method:'清晨练习'})
CREATE (e_454:Exercise {id:'exercise_454', name:'跳绳23', effect:'提升免疫', method:'清晨练习'})
CREATE (e_455:Exercise {id:'exercise_455', name:'爬楼梯23', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_456:Exercise {id:'exercise_456', name:'骑行23', effect:'调理脏腑', method:'每次30分钟'})
CREATE (e_457:Exercise {id:'exercise_457', name:'登山23', effect:'增强体质', method:'饭后1小时'})
CREATE (e_458:Exercise {id:'exercise_458', name:'气功23', effect:'强筋健骨', method:'清晨练习'})
CREATE (e_459:Exercise {id:'exercise_459', name:'导引术23', effect:'改善睡眠', method:'傍晚练习'})
CREATE (e_460:Exercise {id:'exercise_460', name:'八段锦24', effect:'调理脏腑', method:'每周3-5次'})
CREATE (e_461:Exercise {id:'exercise_461', name:'太极拳24', effect:'调理脏腑', method:'每次45分钟'})
CREATE (e_462:Exercise {id:'exercise_462', name:'五禽戏24', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_463:Exercise {id:'exercise_463', name:'易筋经24', effect:'提升免疫', method:'每次45分钟'})
CREATE (e_464:Exercise {id:'exercise_464', name:'六字诀24', effect:'舒缓压力', method:'傍晚练习'})
CREATE (e_465:Exercise {id:'exercise_465', name:'站桩24', effect:'疏通经络', method:'每周3-5次'})
CREATE (e_466:Exercise {id:'exercise_466', name:'散步24', effect:'疏通经络', method:'每次30分钟'})
CREATE (e_467:Exercise {id:'exercise_467', name:'慢跑24', effect:'增强体质', method:'每次45分钟'})
CREATE (e_468:Exercise {id:'exercise_468', name:'快走24', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_469:Exercise {id:'exercise_469', name:'游泳24', effect:'疏通经络', method:'清晨练习'})
CREATE (e_470:Exercise {id:'exercise_470', name:'瑜伽24', effect:'增强体质', method:'饭后1小时'})
CREATE (e_471:Exercise {id:'exercise_471', name:'普拉提24', effect:'舒缓压力', method:'每次45分钟'})
CREATE (e_472:Exercise {id:'exercise_472', name:'健身操24', effect:'平衡阴阳', method:'饭后1小时'})
CREATE (e_473:Exercise {id:'exercise_473', name:'广场舞24', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_474:Exercise {id:'exercise_474', name:'跳绳24', effect:'疏通经络', method:'饭前1小时'})
CREATE (e_475:Exercise {id:'exercise_475', name:'爬楼梯24', effect:'提升免疫', method:'每次30分钟'})
CREATE (e_476:Exercise {id:'exercise_476', name:'骑行24', effect:'强筋健骨', method:'每次45分钟'})
CREATE (e_477:Exercise {id:'exercise_477', name:'登山24', effect:'减肥塑形', method:'饭后1小时'})
CREATE (e_478:Exercise {id:'exercise_478', name:'气功24', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_479:Exercise {id:'exercise_479', name:'导引术24', effect:'强筋健骨', method:'每次45分钟'})
CREATE (e_480:Exercise {id:'exercise_480', name:'八段锦25', effect:'平衡阴阳', method:'清晨练习'})
CREATE (e_481:Exercise {id:'exercise_481', name:'太极拳25', effect:'平衡阴阳', method:'每次20分钟'})
CREATE (e_482:Exercise {id:'exercise_482', name:'五禽戏25', effect:'平衡阴阳', method:'每日1次'})
CREATE (e_483:Exercise {id:'exercise_483', name:'易筋经25', effect:'调理脏腑', method:'每次30分钟'})
CREATE (e_484:Exercise {id:'exercise_484', name:'六字诀25', effect:'调理脏腑', method:'饭前1小时'})
CREATE (e_485:Exercise {id:'exercise_485', name:'站桩25', effect:'强筋健骨', method:'每次30分钟'})
CREATE (e_486:Exercise {id:'exercise_486', name:'散步25', effect:'调理脏腑', method:'每次20分钟'})
CREATE (e_487:Exercise {id:'exercise_487', name:'慢跑25', effect:'疏通经络', method:'清晨练习'})
CREATE (e_488:Exercise {id:'exercise_488', name:'快走25', effect:'强筋健骨', method:'饭前1小时'})
CREATE (e_489:Exercise {id:'exercise_489', name:'游泳25', effect:'调理脏腑', method:'饭后1小时'})
CREATE (e_490:Exercise {id:'exercise_490', name:'瑜伽25', effect:'增强体质', method:'饭后1小时'})
CREATE (e_491:Exercise {id:'exercise_491', name:'普拉提25', effect:'平衡阴阳', method:'每周3-5次'})
CREATE (e_492:Exercise {id:'exercise_492', name:'健身操25', effect:'减肥塑形', method:'每次30分钟'})
CREATE (e_493:Exercise {id:'exercise_493', name:'广场舞25', effect:'减肥塑形', method:'每次20分钟'})
CREATE (e_494:Exercise {id:'exercise_494', name:'跳绳25', effect:'减肥塑形', method:'清晨练习'})
CREATE (e_495:Exercise {id:'exercise_495', name:'爬楼梯25', effect:'减肥塑形', method:'傍晚练习'})
CREATE (e_496:Exercise {id:'exercise_496', name:'骑行25', effect:'减肥塑形', method:'清晨练习'})
CREATE (e_497:Exercise {id:'exercise_497', name:'登山25', effect:'舒缓压力', method:'每周3-5次'})
CREATE (e_498:Exercise {id:'exercise_498', name:'气功25', effect:'减肥塑形', method:'每周3-5次'})
CREATE (e_499:Exercise {id:'exercise_499', name:'导引术25', effect:'改善睡眠', method:'每次20分钟'})
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_79'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_157'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_222'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_332'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_237'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_277'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_352'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_76'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_221'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_88'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_150'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_480'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_90'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_9'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_467'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_373'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_402'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_364'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_476'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_128'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_45'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_271'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_335'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_481'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_496'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_112'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_58'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_64'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_101'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_186'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_336'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_499'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_189'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_175'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_383'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_15'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_268'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_62'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_34'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_215'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_434'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_31'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_325'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_356'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_370'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_32'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_424'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_386'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_94'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_208'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_413'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_404'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_158'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_168'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_431'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_260'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_385'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_320'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_77'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_446'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_247'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_240'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_233'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_97'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (a:Acupoint {id:'acupoint_305'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_30'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_495'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_343'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_276'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_51'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_25'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_463'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_488'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_290'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_360'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_123'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_148'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_221'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_164'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_159'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_396'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_491'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_346'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_220'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_101'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_3'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_156'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_137'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_264'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_288'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_384'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_39'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_483'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_423'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_10'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_239'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_330'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_160'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_114'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_456'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_9'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_281'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_65'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_272'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_236'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_11'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_190'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_334'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_204'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_59'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_79'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_441'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_442'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_317'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_449'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_193'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_321'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_240'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_76'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_450'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_497'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_499'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_475'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_328'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_425'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_229'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_15'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_174'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_222'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (f:Food {id:'food_139'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_314'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_200'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_113'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_72'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_100'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_250'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_135'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_482'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_278'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_226'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_76'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_164'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_462'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_3'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_255'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_264'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_497'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_162'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_233'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_81'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_59'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_197'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_29'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_62'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_498'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_30'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_331'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_333'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_137'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_486'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_450'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_309'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_431'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_367'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_146'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_198'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_61'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_491'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_87'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_235'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_42'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_432'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_141'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_242'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_442'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_31'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_126'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_207'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_39'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_371'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_459'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_183'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_495'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_36'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_251'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_427'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_58'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_147'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_492'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_430'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_439'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_120'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_344'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_489'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_pinghe'}), (e:Exercise {id:'exercise_456'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_319'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_378'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_94'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_163'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_3'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_373'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_211'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_150'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_102'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_82'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_116'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_44'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_36'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_127'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_280'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_178'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_71'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_52'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_214'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_38'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_156'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_372'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_122'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_119'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_405'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_149'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_19'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_187'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_386'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_172'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_84'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_484'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_274'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_477'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_231'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_132'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_117'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_426'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_85'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_362'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_363'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_253'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_437'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_295'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_369'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_468'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_352'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_103'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_392'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_181'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_458'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_192'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_54'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_135'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_7'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_339'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_185'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_364'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_113'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_176'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_64'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_41'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_204'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_77'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (a:Acupoint {id:'acupoint_330'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_68'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_144'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_451'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_284'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_152'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_487'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_126'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_56'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_377'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_444'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_456'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_84'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_234'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_150'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_59'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_137'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_46'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_308'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_408'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_232'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_363'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_403'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_90'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_305'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_270'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_264'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_486'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_470'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_195'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_297'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_76'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_450'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_18'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_123'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_483'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_157'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_132'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_197'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_484'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_469'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_499'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_298'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_120'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_307'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_100'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_293'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_419'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_400'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_201'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_79'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_351'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_317'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_240'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_102'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_495'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_316'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_438'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_398'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_364'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_333'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_339'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_250'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_320'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_319'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (f:Food {id:'food_93'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_245'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_65'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_101'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_393'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_313'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_355'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_235'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_200'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_477'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_323'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_379'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_78'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_6'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_392'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_312'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_210'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_204'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_342'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_98'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_493'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_378'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_211'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_142'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_185'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_218'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_442'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_67'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_488'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_336'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_253'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_205'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_159'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_474'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_147'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_194'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_316'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_231'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_41'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_178'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_306'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_192'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_457'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_144'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_289'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_406'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_150'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_351'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_318'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_24'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_366'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_220'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_131'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_56'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_125'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_268'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_128'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_216'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_340'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_179'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_49'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_50'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_341'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_93'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_203'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qixu'}), (e:Exercise {id:'exercise_31'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_246'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_227'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_37'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_404'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_448'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_331'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_435'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_491'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_215'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_391'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_146'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_250'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_105'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_117'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_259'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_263'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_439'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_447'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_482'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_325'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_322'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_4'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_163'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_280'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_418'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_264'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_49'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_214'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_13'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_389'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_432'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_367'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_253'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_71'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_228'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_182'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_466'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_461'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_77'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_104'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_275'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_308'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_241'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_93'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_341'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_40'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_424'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_251'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_438'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_477'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_22'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_354'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_220'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_10'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_260'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_65'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_48'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_204'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_148'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_362'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_210'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_261'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_411'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_369'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (a:Acupoint {id:'acupoint_176'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_91'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_75'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_249'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_468'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_151'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_354'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_167'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_42'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_347'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_116'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_87'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_445'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_39'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_297'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_54'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_10'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_340'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_213'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_138'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_397'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_81'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_337'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_242'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_444'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_201'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_357'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_85'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_114'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_126'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_279'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_128'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_112'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_41'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_208'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_452'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_154'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_44'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_143'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_222'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_370'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_178'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_315'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_232'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_16'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_273'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_1'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_227'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_474'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_467'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_146'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_240'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_350'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_78'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_186'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_389'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_464'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_443'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_43'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_318'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_106'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_335'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_221'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_496'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_412'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (f:Food {id:'food_169'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_426'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_278'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_154'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_429'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_326'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_188'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_64'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_62'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_81'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_12'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_112'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_178'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_412'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_23'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_44'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_145'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_221'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_113'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_387'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_284'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_333'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_291'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_182'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_244'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_190'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_101'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_8'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_82'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_70'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_27'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_111'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_441'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_350'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_382'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_445'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_222'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_271'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_223'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_462'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_164'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_119'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_471'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_176'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_275'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_458'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_374'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_186'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_9'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_338'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_147'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_411'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_212'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_55'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_18'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_177'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_289'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_296'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_206'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_443'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_174'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_97'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_122'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_272'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_205'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yangxu'}), (e:Exercise {id:'exercise_407'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_347'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_50'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_484'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_345'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_358'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_165'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_202'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_235'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_267'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_469'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_218'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_279'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_105'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_288'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_302'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_211'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_252'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_408'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_286'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_199'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_409'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_236'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_463'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_59'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_280'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_381'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_458'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_460'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_467'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_390'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_376'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_459'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_80'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_456'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_160'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_212'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_357'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_121'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_310'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_295'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_114'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_61'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_158'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_217'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_405'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_9'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_487'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_475'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_226'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_29'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_99'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_178'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_205'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_168'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_319'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_40'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_298'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_372'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_34'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_338'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_294'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_388'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_433'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_7'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (a:Acupoint {id:'acupoint_183'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_38'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_300'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_372'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_28'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_12'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_364'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_158'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_265'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_75'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_0'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_266'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_142'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_313'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_473'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_412'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_390'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_71'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_328'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_344'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_439'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_246'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_472'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_257'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_362'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_239'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_26'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_418'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_242'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_285'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_181'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_308'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_476'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_467'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_438'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_29'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_222'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_135'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_385'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_243'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_210'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_409'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_389'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_159'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_126'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_449'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_287'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_228'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_97'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_354'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_103'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_119'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_63'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_201'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_411'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_50'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_51'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_166'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_487'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_498'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_318'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_87'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_220'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_143'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_283'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (f:Food {id:'food_136'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_23'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_468'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_139'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_395'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_161'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_263'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_141'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_104'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_375'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_217'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_432'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_95'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_354'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_275'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_374'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_47'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_401'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_137'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_338'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_208'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_100'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_252'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_220'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_483'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_304'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_221'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_160'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_91'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_258'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_322'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_117'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_189'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_452'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_59'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_181'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_79'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_429'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_90'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_129'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_440'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_122'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_352'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_194'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_477'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_443'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_9'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_343'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_407'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_107'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_38'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_125'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_170'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_223'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_312'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_261'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_412'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_311'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_355'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_391'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_406'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_420'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_425'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_295'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_218'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_yinxu'}), (e:Exercise {id:'exercise_339'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_490'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_455'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_311'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_10'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_181'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_178'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_415'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_224'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_498'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_74'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_193'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_479'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_20'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_146'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_377'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_494'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_52'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_256'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_376'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_478'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_477'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_280'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_170'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_421'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_422'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_351'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_231'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_378'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_499'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_327'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_84'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_234'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_495'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_155'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_410'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_405'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_383'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_238'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_313'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_394'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_373'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_458'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_474'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_1'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_243'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_200'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_30'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_47'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_304'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_487'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_453'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_245'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_23'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_384'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_31'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_248'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_39'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_251'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_382'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_399'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_0'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_50'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_48'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_491'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (a:Acupoint {id:'acupoint_211'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_431'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_81'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_309'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_480'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_109'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_472'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_239'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_180'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_54'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_186'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_375'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_128'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_395'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_414'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_188'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_110'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_210'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_265'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_314'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_201'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_198'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_2'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_208'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_108'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_112'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_251'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_460'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_437'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_311'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_363'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_331'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_332'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_121'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_488'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_28'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_448'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_334'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_91'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_44'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_412'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_21'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_37'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_335'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_489'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_78'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_380'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_216'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_467'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_294'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_290'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_66'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_310'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_406'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_299'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_155'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_470'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_376'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_304'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_118'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_75'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_429'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_330'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_261'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_173'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (f:Food {id:'food_293'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_368'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_306'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_372'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_101'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_342'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_232'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_308'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_291'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_2'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_344'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_240'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_258'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_120'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_158'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_327'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_261'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_328'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_383'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_100'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_495'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_425'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_462'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_479'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_0'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_449'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_464'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_243'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_466'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_293'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_297'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_480'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_428'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_222'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_37'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_271'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_460'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_352'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_28'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_285'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_408'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_322'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_323'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_499'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_105'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_469'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_61'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_335'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_413'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_283'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_15'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_336'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_195'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_76'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_231'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_492'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_346'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_399'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_417'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_391'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_159'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_488'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_410'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_83'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_124'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tanshi'}), (e:Exercise {id:'exercise_206'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_242'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_298'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_457'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_382'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_337'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_269'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_334'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_175'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_444'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_57'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_263'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_187'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_65'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_365'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_307'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_312'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_215'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_219'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_163'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_157'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_173'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_176'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_451'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_476'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_231'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_445'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_101'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_42'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_11'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_497'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_358'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_226'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_232'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_418'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_265'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_92'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_267'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_386'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_164'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_376'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_21'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_241'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_281'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_177'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_442'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_209'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_435'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_112'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_374'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_245'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_397'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_202'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_8'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_46'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_258'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_198'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_432'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_270'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_308'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_306'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_6'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_179'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_412'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_467'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (a:Acupoint {id:'acupoint_482'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_177'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_156'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_8'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_194'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_190'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_348'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_215'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_77'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_264'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_267'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_27'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_383'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_21'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_198'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_144'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_185'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_227'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_80'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_256'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_344'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_202'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_411'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_345'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_171'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_146'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_399'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_360'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_45'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_468'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_402'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_274'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_141'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_295'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_284'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_343'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_318'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_191'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_304'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_93'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_1'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_174'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_325'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_84'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_175'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_107'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_430'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_221'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_272'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_414'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_277'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_44'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_475'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_179'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_76'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_151'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_462'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_488'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_288'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_367'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_240'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_299'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_210'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_254'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_424'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (f:Food {id:'food_72'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_194'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_375'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_354'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_406'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_459'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_332'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_240'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_245'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_431'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_55'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_493'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_155'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_234'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_110'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_372'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_176'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_319'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_453'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_268'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_21'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_369'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_259'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_230'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_282'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_316'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_203'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_39'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_257'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_362'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_385'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_413'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_212'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_190'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_142'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_198'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_51'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_252'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_309'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_358'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_334'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_249'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_318'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_264'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_219'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_107'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_242'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_403'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_200'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_160'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_483'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_266'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_279'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_6'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_335'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_283'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_141'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_145'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_87'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_127'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_30'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_254'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_146'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_415'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_346'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_shire'}), (e:Exercise {id:'exercise_439'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_215'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_264'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_44'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_46'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_320'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_278'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_375'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_285'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_82'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_43'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_363'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_239'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_271'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_351'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_72'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_97'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_468'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_314'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_24'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_481'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_305'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_483'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_487'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_122'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_316'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_367'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_17'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_211'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_80'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_15'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_81'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_268'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_116'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_417'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_350'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_342'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_20'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_485'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_222'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_57'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_446'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_74'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_451'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_395'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_260'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_394'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_478'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_83'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_243'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_407'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_262'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_391'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_47'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_347'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_279'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_111'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_139'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_147'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_61'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_431'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_190'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_374'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_340'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_471'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (a:Acupoint {id:'acupoint_247'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_1'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_65'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_34'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_28'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_241'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_373'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_360'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_289'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_296'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_114'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_25'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_254'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_310'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_190'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_365'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_131'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_476'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_16'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_235'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_200'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_133'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_317'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_272'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_32'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_354'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_464'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_493'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_211'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_199'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_141'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_299'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_83'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_176'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_152'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_297'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_429'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_333'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_392'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_96'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_390'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_209'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_12'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_137'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_99'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_175'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_66'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_345'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_58'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_290'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_474'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_22'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_326'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_380'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_130'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_21'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_431'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_453'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_243'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_84'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_39'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_382'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_60'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_266'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_436'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (f:Food {id:'food_19'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_6'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_48'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_252'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_280'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_215'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_308'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_135'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_356'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_104'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_313'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_227'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_52'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_253'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_219'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_321'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_206'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_424'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_257'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_353'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_444'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_488'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_35'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_148'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_487'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_418'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_217'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_455'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_449'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_58'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_142'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_157'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_41'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_116'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_354'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_360'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_181'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_3'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_271'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_337'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_23'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_105'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_451'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_266'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_383'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_426'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_447'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_464'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_141'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_149'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_238'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_399'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_155'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_32'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_317'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_125'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_472'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_259'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_118'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_124'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_204'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_214'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_274'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_37'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_405'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_xueyu'}), (e:Exercise {id:'exercise_388'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_491'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_78'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_389'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_408'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_220'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_463'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_130'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_484'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_265'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_344'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_30'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_294'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_159'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_277'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_291'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_70'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_427'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_44'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_398'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_309'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_64'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_106'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_342'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_218'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_240'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_414'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_357'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_374'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_303'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_82'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_402'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_112'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_438'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_483'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_17'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_45'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_231'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_255'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_384'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_107'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_103'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_456'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_486'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_466'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_59'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_85'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_174'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_31'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_200'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_186'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_116'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_94'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_498'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_315'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_481'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_245'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_322'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_124'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_459'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_299'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_421'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_261'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_192'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_366'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (a:Acupoint {id:'acupoint_154'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_325'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_152'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_76'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_377'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_309'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_475'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_311'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_327'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_487'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_263'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_406'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_144'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_485'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_129'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_435'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_344'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_403'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_60'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_192'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_109'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_374'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_135'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_380'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_417'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_242'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_119'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_319'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_294'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_288'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_423'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_171'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_317'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_365'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_445'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_213'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_415'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_480'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_65'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_429'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_368'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_284'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_63'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_326'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_469'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_44'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_383'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_169'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_424'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_251'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_5'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_204'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_280'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_133'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_446'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_363'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_362'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_19'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_29'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_89'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_292'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_40'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_18'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_410'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_281'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (f:Food {id:'food_407'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_391'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_405'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_34'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_438'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_232'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_50'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_484'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_461'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_221'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_302'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_172'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_115'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_317'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_71'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_273'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_475'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_388'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_121'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_18'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_469'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_447'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_466'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_339'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_90'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_459'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_137'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_251'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_26'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_234'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_265'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_278'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_377'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_23'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_494'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_75'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_227'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_77'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_381'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_195'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_223'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_4'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_3'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_212'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_220'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_393'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_67'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_445'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_143'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_322'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_197'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_291'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_303'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_390'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_218'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_437'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_276'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_455'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_299'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_292'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_214'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_358'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_453'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_112'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_356'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_qiyu'}), (e:Exercise {id:'exercise_247'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_373'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_192'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_382'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_395'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_470'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_391'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_341'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_242'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_185'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_179'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_137'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_265'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_456'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_3'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_340'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_261'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_481'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_302'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_142'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_377'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_117'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_304'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_162'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_484'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_220'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_425'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_473'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_432'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_172'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_249'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_49'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_226'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_326'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_281'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_345'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_112'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_320'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_228'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_189'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_266'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_46'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_205'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_148'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_287'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_349'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_388'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_178'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_383'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_68'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_221'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_475'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_290'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_243'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_292'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_424'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_394'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_222'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_156'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_95'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_184'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_227'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_485'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_176'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_81'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (a:Acupoint {id:'acupoint_313'}) CREATE (c)-[:RECOMMEND_ACUPOINT]->(a);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_120'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_369'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_239'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_48'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_360'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_18'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_174'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_123'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_65'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_161'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_112'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_201'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_425'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_224'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_253'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_283'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_478'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_41'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_5'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_459'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_429'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_298'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_278'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_473'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_118'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_138'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_380'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_135'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_121'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_255'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_176'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_203'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_376'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_32'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_42'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_329'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_177'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_378'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_426'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_167'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_316'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_272'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_471'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_81'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_338'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_465'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_399'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_29'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_474'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_444'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_391'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_106'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_314'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_384'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_414'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_54'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_416'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_180'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_382'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_245'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_99'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_492'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_196'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_6'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (f:Food {id:'food_438'}) CREATE (c)-[:RECOMMEND_FOOD]->(f);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_132'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_293'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_97'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_128'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_341'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_154'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_469'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_435'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_183'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_79'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_427'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_262'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_187'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_133'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_233'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_365'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_470'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_27'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_33'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_139'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_238'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_240'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_100'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_476'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_174'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_134'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_281'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_390'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_191'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_307'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_44'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_246'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_425'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_74'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_86'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_111'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_192'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_280'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_382'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_162'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_288'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_498'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_249'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_151'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_442'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_339'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_386'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_466'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_141'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_264'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_421'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_101'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_454'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_335'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_473'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_72'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_313'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_226'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_143'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_395'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_218'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_305'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_49'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_207'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
MATCH (c:Constitution {id:'c_tebing'}), (e:Exercise {id:'exercise_227'}) CREATE (c)-[:RECOMMEND_EXERCISE]->(e);
CREATE (tp_pinghe:TherapyProcess {id:'tp_pinghe', name:'平和质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_pinghe'}), (tp:TherapyProcess {id:'tp_pinghe'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_pinghe_饮食调养:HealthKnowledge {id:'hk_pinghe_饮食调养', type:'平和质', category:'饮食调养', content:'平和质的饮食调养建议'})
MATCH (c:Constitution {id:'c_pinghe'}), (hk:HealthKnowledge {id:'hk_pinghe_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_pinghe_起居调摄:HealthKnowledge {id:'hk_pinghe_起居调摄', type:'平和质', category:'起居调摄', content:'平和质的起居调摄建议'})
MATCH (c:Constitution {id:'c_pinghe'}), (hk:HealthKnowledge {id:'hk_pinghe_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_pinghe_运动保健:HealthKnowledge {id:'hk_pinghe_运动保健', type:'平和质', category:'运动保健', content:'平和质的运动保健建议'})
MATCH (c:Constitution {id:'c_pinghe'}), (hk:HealthKnowledge {id:'hk_pinghe_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_pinghe_药物调养:HealthKnowledge {id:'hk_pinghe_药物调养', type:'平和质', category:'药物调养', content:'平和质的药物调养建议'})
MATCH (c:Constitution {id:'c_pinghe'}), (hk:HealthKnowledge {id:'hk_pinghe_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_qixu:TherapyProcess {id:'tp_qixu', name:'气虚质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_qixu'}), (tp:TherapyProcess {id:'tp_qixu'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_qixu_饮食调养:HealthKnowledge {id:'hk_qixu_饮食调养', type:'气虚质', category:'饮食调养', content:'气虚质的饮食调养建议'})
MATCH (c:Constitution {id:'c_qixu'}), (hk:HealthKnowledge {id:'hk_qixu_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_qixu_起居调摄:HealthKnowledge {id:'hk_qixu_起居调摄', type:'气虚质', category:'起居调摄', content:'气虚质的起居调摄建议'})
MATCH (c:Constitution {id:'c_qixu'}), (hk:HealthKnowledge {id:'hk_qixu_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_qixu_运动保健:HealthKnowledge {id:'hk_qixu_运动保健', type:'气虚质', category:'运动保健', content:'气虚质的运动保健建议'})
MATCH (c:Constitution {id:'c_qixu'}), (hk:HealthKnowledge {id:'hk_qixu_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_qixu_药物调养:HealthKnowledge {id:'hk_qixu_药物调养', type:'气虚质', category:'药物调养', content:'气虚质的药物调养建议'})
MATCH (c:Constitution {id:'c_qixu'}), (hk:HealthKnowledge {id:'hk_qixu_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_yangxu:TherapyProcess {id:'tp_yangxu', name:'阳虚质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_yangxu'}), (tp:TherapyProcess {id:'tp_yangxu'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_yangxu_饮食调养:HealthKnowledge {id:'hk_yangxu_饮食调养', type:'阳虚质', category:'饮食调养', content:'阳虚质的饮食调养建议'})
MATCH (c:Constitution {id:'c_yangxu'}), (hk:HealthKnowledge {id:'hk_yangxu_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_yangxu_起居调摄:HealthKnowledge {id:'hk_yangxu_起居调摄', type:'阳虚质', category:'起居调摄', content:'阳虚质的起居调摄建议'})
MATCH (c:Constitution {id:'c_yangxu'}), (hk:HealthKnowledge {id:'hk_yangxu_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_yangxu_运动保健:HealthKnowledge {id:'hk_yangxu_运动保健', type:'阳虚质', category:'运动保健', content:'阳虚质的运动保健建议'})
MATCH (c:Constitution {id:'c_yangxu'}), (hk:HealthKnowledge {id:'hk_yangxu_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_yangxu_药物调养:HealthKnowledge {id:'hk_yangxu_药物调养', type:'阳虚质', category:'药物调养', content:'阳虚质的药物调养建议'})
MATCH (c:Constitution {id:'c_yangxu'}), (hk:HealthKnowledge {id:'hk_yangxu_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_yinxu:TherapyProcess {id:'tp_yinxu', name:'阴虚质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_yinxu'}), (tp:TherapyProcess {id:'tp_yinxu'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_yinxu_饮食调养:HealthKnowledge {id:'hk_yinxu_饮食调养', type:'阴虚质', category:'饮食调养', content:'阴虚质的饮食调养建议'})
MATCH (c:Constitution {id:'c_yinxu'}), (hk:HealthKnowledge {id:'hk_yinxu_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_yinxu_起居调摄:HealthKnowledge {id:'hk_yinxu_起居调摄', type:'阴虚质', category:'起居调摄', content:'阴虚质的起居调摄建议'})
MATCH (c:Constitution {id:'c_yinxu'}), (hk:HealthKnowledge {id:'hk_yinxu_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_yinxu_运动保健:HealthKnowledge {id:'hk_yinxu_运动保健', type:'阴虚质', category:'运动保健', content:'阴虚质的运动保健建议'})
MATCH (c:Constitution {id:'c_yinxu'}), (hk:HealthKnowledge {id:'hk_yinxu_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_yinxu_药物调养:HealthKnowledge {id:'hk_yinxu_药物调养', type:'阴虚质', category:'药物调养', content:'阴虚质的药物调养建议'})
MATCH (c:Constitution {id:'c_yinxu'}), (hk:HealthKnowledge {id:'hk_yinxu_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_tanshi:TherapyProcess {id:'tp_tanshi', name:'痰湿质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_tanshi'}), (tp:TherapyProcess {id:'tp_tanshi'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_tanshi_饮食调养:HealthKnowledge {id:'hk_tanshi_饮食调养', type:'痰湿质', category:'饮食调养', content:'痰湿质的饮食调养建议'})
MATCH (c:Constitution {id:'c_tanshi'}), (hk:HealthKnowledge {id:'hk_tanshi_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_tanshi_起居调摄:HealthKnowledge {id:'hk_tanshi_起居调摄', type:'痰湿质', category:'起居调摄', content:'痰湿质的起居调摄建议'})
MATCH (c:Constitution {id:'c_tanshi'}), (hk:HealthKnowledge {id:'hk_tanshi_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_tanshi_运动保健:HealthKnowledge {id:'hk_tanshi_运动保健', type:'痰湿质', category:'运动保健', content:'痰湿质的运动保健建议'})
MATCH (c:Constitution {id:'c_tanshi'}), (hk:HealthKnowledge {id:'hk_tanshi_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_tanshi_药物调养:HealthKnowledge {id:'hk_tanshi_药物调养', type:'痰湿质', category:'药物调养', content:'痰湿质的药物调养建议'})
MATCH (c:Constitution {id:'c_tanshi'}), (hk:HealthKnowledge {id:'hk_tanshi_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_shire:TherapyProcess {id:'tp_shire', name:'湿热质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_shire'}), (tp:TherapyProcess {id:'tp_shire'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_shire_饮食调养:HealthKnowledge {id:'hk_shire_饮食调养', type:'湿热质', category:'饮食调养', content:'湿热质的饮食调养建议'})
MATCH (c:Constitution {id:'c_shire'}), (hk:HealthKnowledge {id:'hk_shire_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_shire_起居调摄:HealthKnowledge {id:'hk_shire_起居调摄', type:'湿热质', category:'起居调摄', content:'湿热质的起居调摄建议'})
MATCH (c:Constitution {id:'c_shire'}), (hk:HealthKnowledge {id:'hk_shire_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_shire_运动保健:HealthKnowledge {id:'hk_shire_运动保健', type:'湿热质', category:'运动保健', content:'湿热质的运动保健建议'})
MATCH (c:Constitution {id:'c_shire'}), (hk:HealthKnowledge {id:'hk_shire_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_shire_药物调养:HealthKnowledge {id:'hk_shire_药物调养', type:'湿热质', category:'药物调养', content:'湿热质的药物调养建议'})
MATCH (c:Constitution {id:'c_shire'}), (hk:HealthKnowledge {id:'hk_shire_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_xueyu:TherapyProcess {id:'tp_xueyu', name:'血瘀质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_xueyu'}), (tp:TherapyProcess {id:'tp_xueyu'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_xueyu_饮食调养:HealthKnowledge {id:'hk_xueyu_饮食调养', type:'血瘀质', category:'饮食调养', content:'血瘀质的饮食调养建议'})
MATCH (c:Constitution {id:'c_xueyu'}), (hk:HealthKnowledge {id:'hk_xueyu_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_xueyu_起居调摄:HealthKnowledge {id:'hk_xueyu_起居调摄', type:'血瘀质', category:'起居调摄', content:'血瘀质的起居调摄建议'})
MATCH (c:Constitution {id:'c_xueyu'}), (hk:HealthKnowledge {id:'hk_xueyu_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_xueyu_运动保健:HealthKnowledge {id:'hk_xueyu_运动保健', type:'血瘀质', category:'运动保健', content:'血瘀质的运动保健建议'})
MATCH (c:Constitution {id:'c_xueyu'}), (hk:HealthKnowledge {id:'hk_xueyu_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_xueyu_药物调养:HealthKnowledge {id:'hk_xueyu_药物调养', type:'血瘀质', category:'药物调养', content:'血瘀质的药物调养建议'})
MATCH (c:Constitution {id:'c_xueyu'}), (hk:HealthKnowledge {id:'hk_xueyu_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_qiyu:TherapyProcess {id:'tp_qiyu', name:'气郁质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_qiyu'}), (tp:TherapyProcess {id:'tp_qiyu'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_qiyu_饮食调养:HealthKnowledge {id:'hk_qiyu_饮食调养', type:'气郁质', category:'饮食调养', content:'气郁质的饮食调养建议'})
MATCH (c:Constitution {id:'c_qiyu'}), (hk:HealthKnowledge {id:'hk_qiyu_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_qiyu_起居调摄:HealthKnowledge {id:'hk_qiyu_起居调摄', type:'气郁质', category:'起居调摄', content:'气郁质的起居调摄建议'})
MATCH (c:Constitution {id:'c_qiyu'}), (hk:HealthKnowledge {id:'hk_qiyu_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_qiyu_运动保健:HealthKnowledge {id:'hk_qiyu_运动保健', type:'气郁质', category:'运动保健', content:'气郁质的运动保健建议'})
MATCH (c:Constitution {id:'c_qiyu'}), (hk:HealthKnowledge {id:'hk_qiyu_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_qiyu_药物调养:HealthKnowledge {id:'hk_qiyu_药物调养', type:'气郁质', category:'药物调养', content:'气郁质的药物调养建议'})
MATCH (c:Constitution {id:'c_qiyu'}), (hk:HealthKnowledge {id:'hk_qiyu_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (tp_tebing:TherapyProcess {id:'tp_tebing', name:'特禀质艾灸疗法', base:'清洁皮肤', sequence:'穴位顺序', frequency:'每周3次'})
MATCH (c:Constitution {id:'c_tebing'}), (tp:TherapyProcess {id:'tp_tebing'}) CREATE (c)-[:HAS_THERAPY]->(tp);
CREATE (hk_tebing_饮食调养:HealthKnowledge {id:'hk_tebing_饮食调养', type:'特禀质', category:'饮食调养', content:'特禀质的饮食调养建议'})
MATCH (c:Constitution {id:'c_tebing'}), (hk:HealthKnowledge {id:'hk_tebing_饮食调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_tebing_起居调摄:HealthKnowledge {id:'hk_tebing_起居调摄', type:'特禀质', category:'起居调摄', content:'特禀质的起居调摄建议'})
MATCH (c:Constitution {id:'c_tebing'}), (hk:HealthKnowledge {id:'hk_tebing_起居调摄'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_tebing_运动保健:HealthKnowledge {id:'hk_tebing_运动保健', type:'特禀质', category:'运动保健', content:'特禀质的运动保健建议'})
MATCH (c:Constitution {id:'c_tebing'}), (hk:HealthKnowledge {id:'hk_tebing_运动保健'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
CREATE (hk_tebing_药物调养:HealthKnowledge {id:'hk_tebing_药物调养', type:'特禀质', category:'药物调养', content:'特禀质的药物调养建议'})
MATCH (c:Constitution {id:'c_tebing'}), (hk:HealthKnowledge {id:'hk_tebing_药物调养'}) CREATE (c)-[:HAS_KNOWLEDGE]->(hk);
MATCH (n) RETURN labels(n) AS 类型, count(n) AS 数量;