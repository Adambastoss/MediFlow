CREATE DATABASE MEDIFLOW;

CREATE TABLE PROCEDIMENTOS(
ID INT PRIMARY KEY AUTO_INCREMENT,
NOME VARCHAR(100) NOT NULL,
CATEGORIA ENUM('CONSULTA', 'EXAME LABORATORIAL', 'EXAME DE IMAGEM', 'VACINA') NOT NULL,
PRECO DECIMAL(10, 2) NOT NULL,
DESCRICAO TEXT,
ATIVO BOOLEAN DEFAULT TRUE,
TEMPO_ESTIMADO TIME
);

INSERT INTO PROCEDIMENTOS (NOME, CATEGORIA, PRECO, DESCRICAO, TEMPO_ESTIMADO) VALUES
('Consulta Clínica Geral', 'CONSULTA', 120.00, 'Consulta de rotina com médico clínico geral.', '00:30:00'),
('Hemograma Completo', 'EXAME LABORATORIAL', 85.50, 'Exame de sangue para avaliação geral da saúde.', '00:15:00'),
('Raio-X Tórax', 'EXAME DE IMAGEM', 150.75, 'Radiografia da região torácica para diagnóstico de diversas condições.', '00:20:00'),
('Vacina Antigripal', 'VACINA', 60.00, 'Vacina contra o vírus Influenza (gripe).', '00:10:00'),
('Consulta com Cardiologista', 'CONSULTA', 250.00, 'Consulta especializada com médico cardiologista.', '00:45:00'),
('Glicemia em Jejum', 'EXAME LABORATORIAL', 35.20, 'Exame para medir o nível de glicose no sangue após jejum.', '00:05:00'),
('Ultrassonografia Abdominal', 'EXAME DE IMAGEM', 220.90, 'Exame de imagem para visualização dos órgãos internos do abdômen.', '00:35:00'),
('Vacina Tríplice Viral (Sarampo, Caxumba, Rubéola)', 'VACINA', 95.00, 'Vacina combinada contra sarampo, caxumba e rubéola.', '00:15:00'),
('Consulta com Dermatologista', 'CONSULTA', 180.50, 'Consulta especializada com médico dermatologista.', '00:40:00'),
('Cultura de Urina', 'EXAME LABORATORIAL', 70.00, 'Exame laboratorial para identificar bactérias em amostra de urina.', '00:25:00');



	