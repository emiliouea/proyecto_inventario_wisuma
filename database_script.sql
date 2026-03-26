-- ============================================================
-- Script SQL - Ferretería Senguana
-- Base de datos: proyecto_inventario_wisuma
-- ============================================================

CREATE DATABASE IF NOT EXISTS proyecto_inventario_wisuma
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE proyecto_inventario_wisuma;

-- ------------------------------------------------------------
-- Tabla: usuarios
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario  INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL
);

-- ------------------------------------------------------------
-- Tabla: producto
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS producto (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    categoria       VARCHAR(50)  NOT NULL DEFAULT 'General',
    descripcion     VARCHAR(200),
    precio          DOUBLE       NOT NULL,
    stock           INT          NOT NULL DEFAULT 0,
    fecha_creacion  DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Tabla: cliente
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cliente (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    telefono    VARCHAR(20),
    email       VARCHAR(100),
    tipo        VARCHAR(50)  DEFAULT 'Particular'
);

-- ------------------------------------------------------------
-- Tabla: facturas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facturas (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id  INT    NOT NULL,
    fecha       DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado      VARCHAR(20) DEFAULT 'Pendiente',
    total       DOUBLE DEFAULT 0.0,
    CONSTRAINT fk_factura_cliente FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- ------------------------------------------------------------
-- Tabla: factura_detalles
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS factura_detalles (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    factura_id      INT    NOT NULL,
    producto_id     INT    NOT NULL,
    cantidad        INT    NOT NULL,
    precio_unitario DOUBLE NOT NULL,
    subtotal        DOUBLE NOT NULL,
    CONSTRAINT fk_detalle_factura  FOREIGN KEY (factura_id)  REFERENCES facturas(id) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto FOREIGN KEY (producto_id) REFERENCES producto(id)
);

-- ------------------------------------------------------------
-- Datos de ejemplo
-- ------------------------------------------------------------
INSERT IGNORE INTO usuarios (nombre, email, password) VALUES
('Administrador', 'admin@ferreteria.com', 'pbkdf2:sha256:placeholder');

INSERT IGNORE INTO producto (nombre, categoria, descripcion, precio, stock) VALUES
('Martillo de Carpintero', 'Herramientas Manuales', 'Martillo de acero con mango de madera', 12.50, 50),
('Taladro Eléctrico 500W', 'Herramientas Eléctricas', 'Taladro percutor 500W con maletín', 89.99, 20),
('Cemento Portland 50kg', 'Materiales de Construcción', 'Saco de cemento gris 50kg', 8.75, 200),
('Llave Inglesa 12"', 'Herramientas Manuales', 'Llave ajustable de 12 pulgadas', 15.00, 35),
('Cable Eléctrico 2.5mm x 100m', 'Electricidad', 'Rollo de cable THW 2.5mm', 45.00, 15),
('Pintura Látex Blanco 4L', 'Pintura', 'Pintura interior látex blanco 4 litros', 22.00, 40),
('Tornillos Autorroscantes 1" x100', 'Fijaciones y Tornillería', 'Caja de 100 tornillos autorroscantes', 3.50, 300),
('Tubo PVC 1/2" x 3m', 'Plomería', 'Tubo PVC presión 1/2 pulgada', 4.20, 120);

INSERT IGNORE INTO cliente (nombre, telefono, email, tipo) VALUES
('Juan Pérez', '0991234567', 'juan@email.com', 'Particular'),
('Constructora ABC', '0987654321', 'contacto@abc.com', 'Empresa'),
('María González', '0976543210', 'maria@email.com', 'Particular');
