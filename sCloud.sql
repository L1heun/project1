create table user_account  (
  user_idx INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  user_id VARCHAR(64) NOT NULL UNIQUE KEY,
  user_passwd VARCHAR(255) NOT NULL,
  user_token VARCHAR(255),
  user_signup_time DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
  user_type ENUM('admin',  'normal') NOT NULL DEFAULT 'normal'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table folder(
  folder_idx INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  user_idx INTEGER NOT NULL,
  folder_name VARCHAR(64) NOT NULL DEFAULT '..',
  folder_init_date DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
  FOREIGN KEY (user_idx) REFERENCES user_account (user_idx) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table files(
  file_idx INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  user_idx INTEGER NOT NULL,
  folder_idx INTEGER,
  file_origin_name VARCHAR(64) NOT NULL,
  file_type ENUM('file',  'movie', 'music', 'image') DEFAULT 'file',
  file_is_shared BOOLEAN NOT NULL DEFAULT '0',
  folder_init_date DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
  FOREIGN KEY (user_idx) REFERENCES user_account (user_idx) ON DELETE CASCADE,
  FOREIGN KEY (folder_idx) REFERENCES folder (folder_idx) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table category_db (
  category_idx INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  category_name VARCHAR(64) NOT NULL,
  category_description MEDIUMTEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table category_list (
  folder_idx INTEGER,
  category_idx INTEGER,
  FOREIGN KEY (folder_idx) REFERENCES folder (folder_idx) ON DELETE CASCADE,
  FOREIGN KEY (category_idx) REFERENCES category_db (category_idx) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;