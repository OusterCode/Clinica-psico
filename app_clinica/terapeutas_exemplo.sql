-- Script para inserir 20 terapeutas fictícios na tabela app_clinica_therapist
-- Ajuste os treatments conforme necessário após inserir (ManyToMany)

INSERT INTO app_clinica_therapist
(name, email, telephone, cpf, birth_date, photo, CEP, address, city, state, numero, degree, is_subleasing, hourly_rate, available_days, available_times)
VALUES
('Terapeuta 1', 'terapeuta1@email.com', '(11) 90000-1001', '10000000001', '1985-01-01', NULL, '02001000', 'Rua T1', 'Cidade T1', 'SP', '201', 'Psicologia', 0, 150.00, 'Seg, Qua', '08:00-12:00'),
('Terapeuta 2', 'terapeuta2@email.com', '(11) 90000-1002', '10000000002', '1985-01-02', NULL, '02001001', 'Rua T2', 'Cidade T2', 'SP', '202', 'Psicologia', 1, 180.00, 'Ter, Qui', '13:00-17:00'),
('Terapeuta 3', 'terapeuta3@email.com', '(11) 90000-1003', '10000000003', '1985-01-03', NULL, '02001002', 'Rua T3', 'Cidade T3', 'SP', '203', 'Psicologia', 0, 200.00, 'Sex', '09:00-12:00'),
('Terapeuta 4', 'terapeuta4@email.com', '(11) 90000-1004', '10000000004', '1985-01-04', NULL, '02001003', 'Rua T4', 'Cidade T4', 'SP', '204', 'Psicologia', 1, 170.00, 'Seg, Sex', '14:00-18:00'),
('Terapeuta 5', 'terapeuta5@email.com', '(11) 90000-1005', '10000000005', '1985-01-05', NULL, '02001004', 'Rua T5', 'Cidade T5', 'SP', '205', 'Psicologia', 0, 160.00, 'Ter, Qua', '08:00-11:00'),
('Terapeuta 6', 'terapeuta6@email.com', '(11) 90000-1006', '10000000006', '1985-01-06', NULL, '02001005', 'Rua T6', 'Cidade T6', 'SP', '206', 'Psicologia', 1, 190.00, 'Qua, Sex', '10:00-13:00'),
('Terapeuta 7', 'terapeuta7@email.com', '(11) 90000-1007', '10000000007', '1985-01-07', NULL, '02001006', 'Rua T7', 'Cidade T7', 'SP', '207', 'Psicologia', 0, 175.00, 'Seg, Ter', '15:00-19:00'),
('Terapeuta 8', 'terapeuta8@email.com', '(11) 90000-1008', '10000000008', '1985-01-08', NULL, '02001007', 'Rua T8', 'Cidade T8', 'SP', '208', 'Psicologia', 1, 210.00, 'Qua', '08:00-12:00'),
('Terapeuta 9', 'terapeuta9@email.com', '(11) 90000-1009', '10000000009', '1985-01-09', NULL, '02001008', 'Rua T9', 'Cidade T9', 'SP', '209', 'Psicologia', 0, 155.00, 'Qui, Sex', '13:00-16:00'),
('Terapeuta 10', 'terapeuta10@email.com', '(11) 90000-1010', '10000000010', '1985-01-10', NULL, '02001009', 'Rua T10', 'Cidade T10', 'SP', '210', 'Psicologia', 1, 185.00, 'Seg, Qua', '09:00-12:00'),
('Terapeuta 11', 'terapeuta11@email.com', '(11) 90000-1011', '10000000011', '1985-01-11', NULL, '02001010', 'Rua T11', 'Cidade T11', 'SP', '211', 'Psicologia', 0, 165.00, 'Ter, Sex', '14:00-18:00'),
('Terapeuta 12', 'terapeuta12@email.com', '(11) 90000-1012', '10000000012', '1985-01-12', NULL, '02001011', 'Rua T12', 'Cidade T12', 'SP', '212', 'Psicologia', 1, 195.00, 'Qua, Qui', '08:00-11:00'),
('Terapeuta 13', 'terapeuta13@email.com', '(11) 90000-1013', '10000000013', '1985-01-13', NULL, '02001012', 'Rua T13', 'Cidade T13', 'SP', '213', 'Psicologia', 0, 170.00, 'Seg, Qui', '10:00-13:00'),
('Terapeuta 14', 'terapeuta14@email.com', '(11) 90000-1014', '10000000014', '1985-01-14', NULL, '02001013', 'Rua T14', 'Cidade T14', 'SP', '214', 'Psicologia', 1, 180.00, 'Ter, Qua', '15:00-19:00'),
('Terapeuta 15', 'terapeuta15@email.com', '(11) 90000-1015', '10000000015', '1985-01-15', NULL, '02001014', 'Rua T15', 'Cidade T15', 'SP', '215', 'Psicologia', 0, 200.00, 'Sex', '08:00-12:00'),
('Terapeuta 16', 'terapeuta16@email.com', '(11) 90000-1016', '10000000016', '1985-01-16', NULL, '02001015', 'Rua T16', 'Cidade T16', 'SP', '216', 'Psicologia', 1, 210.00, 'Seg, Sex', '13:00-16:00'),
('Terapeuta 17', 'terapeuta17@email.com', '(11) 90000-1017', '10000000017', '1985-01-17', NULL, '02001016', 'Rua T17', 'Cidade T17', 'SP', '217', 'Psicologia', 0, 155.00, 'Ter, Qua', '09:00-12:00'),
('Terapeuta 18', 'terapeuta18@email.com', '(11) 90000-1018', '10000000018', '1985-01-18', NULL, '02001017', 'Rua T18', 'Cidade T18', 'SP', '218', 'Psicologia', 1, 185.00, 'Qua, Sex', '14:00-18:00'),
('Terapeuta 19', 'terapeuta19@email.com', '(11) 90000-1019', '10000000019', '1985-01-19', NULL, '02001018', 'Rua T19', 'Cidade T19', 'SP', '219', 'Psicologia', 0, 175.00, 'Seg, Qui', '08:00-11:00'),
('Terapeuta 20', 'terapeuta20@email.com', '(11) 90000-1020', '10000000020', '1985-01-20', NULL, '02001019', 'Rua T20', 'Cidade T20', 'SP', '220', 'Psicologia', 1, 190.00, 'Ter, Sex', '10:00-13:00');


