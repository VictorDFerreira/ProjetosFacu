-- Criação da tabela users
CREATE TABLE IF NOT EXISTS users (
  id INT(11) NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
);

-- Criação da tabela appointments com a coluna user_id
CREATE TABLE IF NOT EXISTS appointments (
  id INT(11) NOT NULL AUTO_INCREMENT,
  date DATE DEFAULT NULL,
  period VARCHAR(255) DEFAULT NULL,
  time TIME DEFAULT NULL,
  services TEXT,
  user_id INT(11),  -- Adicionando a coluna user_id
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id)  -- Definindo a chave estrangeira
);
