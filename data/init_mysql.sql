CREATE DATABASE IF NOT EXISTS tcm_health CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tcm_health;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    constitution_type VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    order_num INT NOT NULL
);

CREATE TABLE assessment_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    answers JSON NOT NULL,
    primary_type VARCHAR(20) NOT NULL,
    secondary_types JSON,
    scores JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 插入王琦量表题目（每个体质8题，共72题）
INSERT INTO questions (constitution_type, content, order_num) VALUES
-- 平和质
('pinghe', '您精力充沛吗？', 1),
('pinghe', '您容易疲乏吗？', 2),
('pinghe', '您说话声音低弱无力吗？', 3),
('pinghe', '您感到闷闷不乐、情绪低沉吗？', 4),
('pinghe', '您比一般人耐受不了寒冷（冬天的寒冷，夏天的冷空调、电扇等）吗？', 5),
('pinghe', '您能适应外界自然和社会环境的变化吗？', 6),
('pinghe', '您容易失眠吗？', 7),
('pinghe', '您容易忘事（健忘）吗？', 8),

-- 气虚质
('qixu', '您容易疲乏吗？', 1),
('qixu', '您容易气短（呼吸短促，接不上气）吗？', 2),
('qixu', '您容易心慌吗？', 3),
('qixu', '您容易头晕或站起时晕眩吗？', 4),
('qixu', '您比别人容易患感冒吗？', 5),
('qixu', '您喜欢安静、懒得说话吗？', 6),
('qixu', '您说话声音低弱无力吗？', 7),
('qixu', '您活动量稍大就容易出虚汗吗？', 8),

-- 阳虚质
('yangxu', '您手脚发凉吗？', 1),
('yangxu', '您胃脘部、背部或腰膝部怕冷吗？', 2),
('yangxu', '您感到怕冷、衣服比别人穿得多吗？', 3),
('yangxu', '您比一般人耐受不了寒冷（冬天的寒冷，夏天的冷空调、电扇等）吗？', 4),
('yangxu', '您比别人容易患感冒吗？', 5),
('yangxu', '您吃（喝）凉的东西会感到不舒服或者怕吃（喝）凉东西吗？', 6),
('yangxu', '您受凉或吃（喝）凉的东西后，容易腹泻（拉肚子）吗？', 7),
('yangxu', '您小便次数多或者量多，颜色清，晚上尤其明显吗？', 8),

-- 阴虚质
('yinxu', '您感到手脚心发热吗？', 1),
('yinxu', '您感觉身体、脸上发热吗？', 2),
('yinxu', '您皮肤或口唇干吗？', 3),
('yinxu', '您口唇的颜色比一般人红吗？', 4),
('yinxu', '您容易便秘或大便干燥吗？', 5),
('yinxu', '您面部两颧潮红或偏红吗？', 6),
('yinxu', '您感到眼睛干涩吗？', 7),
('yinxu', '您感到口干咽燥、总想喝水吗？', 8),

-- 痰湿质
('tanshi', '您感到胸闷或腹部胀满吗？', 1),
('tanshi', '您感到身体沉重不轻松或不爽快吗？', 2),
('tanshi', '您腹部肥满松软吗？', 3),
('tanshi', '您有额部油脂分泌多的现象吗？', 4),
('tanshi', '您上眼睑比别人肿（上眼睑有轻微隆起的现象）吗？', 5),
('tanshi', '您嘴里有黏黏的感觉吗？', 6),
('tanshi', '您平时痰多吗？', 7),
('tanshi', '您舌苔厚腻或有舌苔厚厚的感觉吗？', 8),

-- 湿热质
('shire', '您面部或鼻部有油腻感或者油亮发光吗？', 1),
('shire', '您容易生痤疮或者疮疖吗？', 2),
('shire', '您感到口苦或嘴里有异味吗？', 3),
('shire', '您大便黏滞不爽、有解不尽的感觉吗？', 4),
('shire', '您小便时尿道有发热感、尿色浓（深）吗？', 5),
('shire', '您带下色黄（白带颜色发黄）吗？（男士：您的阴囊部位潮湿吗？）', 6),
('shire', '您情绪急躁易怒吗？', 7),
('shire', '您容易觉得身体困重疲倦吗？', 8),

-- 血瘀质
('xueyu', '您的皮肤在不知不觉中会出现青紫瘀斑（皮下出血）吗？', 1),
('xueyu', '您两颧部有细微红丝吗？', 2),
('xueyu', '您身体上有哪里疼痛吗？', 3),
('xueyu', '您面色晦黯或容易出现褐斑吗？', 4),
('xueyu', '您容易有黑眼圈吗？', 5),
('xueyu', '您容易忘事（健忘）吗？', 6),
('xueyu', '您口唇颜色偏黯吗？', 7),
('xueyu', '您舌下静脉有瘀紫或增粗吗？（可观察）', 8),

-- 气郁质
('qiyu', '您感到闷闷不乐、情绪低沉吗？', 1),
('qiyu', '您容易精神紧张、焦虑不安吗？', 2),
('qiyu', '您多愁善感、感情脆弱吗？', 3),
('qiyu', '您容易感到害怕或受到惊吓吗？', 4),
('qiyu', '您胁肋部或乳房胀痛吗？', 5),
('qiyu', '您无缘无故叹气吗？', 6),
('qiyu', '您咽喉部有异物感，且吐之不出、咽之不下吗？', 7),
('qiyu', '您睡眠不好、容易失眠吗？', 8),

-- 特禀质
('tebing', '您没有感冒时也会打喷嚏吗？', 1),
('tebing', '您没有感冒时也会鼻塞、流鼻涕吗？', 2),
('tebing', '您有因季节变化、温度变化或异味等原因而咳喘的现象吗？', 3),
('tebing', '您容易过敏（对药物、食物、气味、花粉等）吗？', 4),
('tebing', '您的皮肤容易起荨麻疹（风团、风疹块）吗？', 5),
('tebing', '您的皮肤因过敏出现过紫癜（紫红色瘀点、瘀斑）吗？', 6),
('tebing', '您的皮肤一抓就红，并出现抓痕吗？', 7),
('tebing', '您有家族遗传病史或先天生理缺陷吗？', 8);