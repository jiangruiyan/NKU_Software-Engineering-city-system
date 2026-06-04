/*
 Navicat Premium Data Transfer

 Source Server         : CitySystem
 Source Server Type    : MySQL
 Source Server Version : 80019 (8.0.19)
 Source Host           : localhost:3306
 Source Schema         : city_system

 Target Server Type    : MySQL
 Target Server Version : 80019 (8.0.19)
 File Encoding         : 65001

 Date: 05/06/2026 00:39:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for assets
-- ----------------------------
DROP TABLE IF EXISTS `assets`;
CREATE TABLE `assets`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` enum('plugin','model','texture') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `submitted_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT (now()),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_assets_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of assets
-- ----------------------------
INSERT INTO `assets` VALUES (1, '路灯-现代款', 'model', 'approved', 'modeler01', '适用于城市主干道的现代路灯3D模型', '2026-05-31 21:48:50');
INSERT INTO `assets` VALUES (2, '沥青路面贴图', 'texture', 'pending', 'modeler01', '高精度沥青路面PBR贴图', '2026-05-31 21:48:50');
INSERT INTO `assets` VALUES (3, '城市植被插件', 'plugin', 'approved', 'modeler01', '自动生成行道树的Blender插件', '2026-05-31 21:48:50');
INSERT INTO `assets` VALUES (4, '公交站台模型', 'model', 'rejected', 'modeler01', '标准公交站台3D模型', '2026-05-31 21:48:50');
INSERT INTO `assets` VALUES (5, '楼房生成插件', 'plugin', 'pending', 'modeler01', '自动生成楼房', '2026-06-04 21:36:15');

-- ----------------------------
-- Table structure for scene_templates
-- ----------------------------
DROP TABLE IF EXISTS `scene_templates`;
CREATE TABLE `scene_templates`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `template_no` int NOT NULL,
  `tree_count` int NULL DEFAULT NULL,
  `road_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `seat_count` int NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT (now()),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `template_no`(`template_no` ASC) USING BTREE,
  INDEX `ix_scene_templates_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of scene_templates
-- ----------------------------
INSERT INTO `scene_templates` VALUES (1, '滨海商业街', 1, 10, 'standard', 5, '', 'modeler01', '2026-06-04 22:25:40');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hashed_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('admin','analyst','modeler') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin01', '$2b$12$OGpDAAi/bBWOVtzE5ZpTl.O/pbTZ6xJrL3N.zLg4kJtztCpVDBRQG', 'admin', '2026-05-31 21:16:49');
INSERT INTO `users` VALUES (2, 'analyst01', '$2b$12$8WY96lj8DewSVCuYKlFoCe9p.fh65AZdE5Z.OsDmp.wNuQxQtlhvO', 'analyst', '2026-05-31 21:16:49');
INSERT INTO `users` VALUES (3, 'modeler01', '$2b$12$dZqgAFzv20q7cxQRB3/.Eu/uZdZbY3QziPp9p38jAkrPDLogQOlQG', 'modeler', '2026-05-31 21:16:49');
INSERT INTO `users` VALUES (4, 'testtest', '$2b$12$TzvyWcDkEW9J/ebLgusmweSZrbVBVF9l5vDauVwDUAvLB321OnXbq', 'analyst', '2026-06-04 21:38:46');

SET FOREIGN_KEY_CHECKS = 1;
