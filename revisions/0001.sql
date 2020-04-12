CREATE SEQUENCE images_sequence START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE images_properties_types_sequence START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE images_properties_sequence START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE models_sequence START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE models_properties_types_sequence START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE models_properties_sequence START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE users_sequence START WITH 1 INCREMENT BY 1;

CREATE TABLE "users" (
  "pk_user" integer PRIMARY KEY DEFAULT nextval('users_sequence'),
  "customer_uid" varchar NOT NULL,
  "email" varchar NOT NULL,
  "username" varchar NOT NULL,
  "password" varchar NOT NULL,
  "created" timestamp with time zone
);


CREATE TABLE "images"(
	"pk_image" integer PRIMARY KEY DEFAULT nextval('images_sequence'),
	"fk_model" integer ,
	"fk_user" integer,
	"created" timestamp with time zone
);


CREATE TABLE "images_properties_types" (
  "pk_image_property_type" integer PRIMARY KEY DEFAULT nextval('images_properties_types_sequence'),
  "key" varchar NOT NULL,
  "description" varchar NOT NULL
);

CREATE TABLE "images_properties" (
  "pk_image_property" integer PRIMARY KEY DEFAULT nextval('images_properties_sequence'),
  "fk_image" integer,
  "fk_image_property_type" integer,
  "value" varchar
);



CREATE TABLE "models"(
	"pk_model" integer PRIMARY KEY DEFAULT nextval('models_sequence'),
	"model_name" varchar,
	"type" varchar
);

CREATE TABLE "models_properties_types"(
	"pk_model_property_type" integer PRIMARY KEY DEFAULT nextval('models_properties_types_sequence'),
	"key" varchar NOT NULL,
	"value" varchar NOT NULL
);

CREATE TABLE "models_properties"(
	"pk_model_property" integer PRIMARY KEY DEFAULT nextval('models_properties_sequence'),
	"fk_model" integer,
	"fk_model_property_type" integer,
	"value" integer
);



ALTER TABLE "images" ADD FOREIGN KEY ("fk_user") REFERENCES "users" ("pk_user");
ALTER TABLE "images" ADD FOREIGN KEY ("fk_model") REFERENCES "models" ("pk_model");
ALTER TABLE "images_properties" ADD FOREIGN KEY ("fk_image_property_type") REFERENCES "images_properties_types" ("pk_image_property_type");
ALTER TABLE "models_properties" ADD FOREIGN KEY ("fk_model") REFERENCES "models" ("pk_model");
ALTER TABLE "models_properties" ADD FOREIGN KEY ("fk_model_property_type") REFERENCES "models_properties_types" ("pk_model_property_type");
ALTER TABLE "images_properties" ADD FOREIGN KEY ("fk_image") REFERENCES "images" ("pk_image");

insert into images_properties_types values (1,'image_processed','Image Processed');
insert into models values(1,'PPEModel','mobilenet_ssd_v2_coco');

ALTER TABLE images
ADD COLUMN image varchar;

CREATE SEQUENCE ppe_compliances_sequence START WITH 1 INCREMENT BY 1;

CREATE TABLE "ppe_compliances"(
	"pk_ppe_compliance" integer PRIMARY KEY DEFAULT nextval('ppe_compliances_sequence'),
	"fk_image" integer ,
	"result_image" varchar,
	"created" timestamp with time zone
);

ALTER TABLE "ppe_compliances" ADD FOREIGN KEY ("fk_image") REFERENCES "images" ("pk_image");

CREATE SEQUENCE ppe_compliances_properties_sequence START WITH 1 INCREMENT BY 1;

CREATE TABLE "ppe_compliances_properties"(
	"pk_ppe_compliance_property" integer PRIMARY KEY DEFAULT nextval('ppe_compliances_properties_sequence'),
	"fk_ppe_compliance" integer ,
	"fk_image_property_type" integer,
	"value" varchar
);

ALTER TABLE "ppe_compliances_properties" ADD FOREIGN KEY ("fk_ppe_compliance") REFERENCES "ppe_compliances" ("pk_ppe_compliance");
ALTER TABLE "ppe_compliances_properties" ADD FOREIGN KEY ("fk_image_property_type") REFERENCES "images_properties_types" ("pk_image_property_type");





