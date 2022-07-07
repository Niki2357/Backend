create table lost_and_found
(
	uuid text not null
		constraint lost_pk
			primary key,
	item_name text not null,
	lost_or_found boolean not null,
	user_id text not null,
	location text not null,
	description text,
	lf_time datetime not null,
	post_time datetime not null,
	image text,
	completed boolean not null,
	item_type text not null
);

create unique index lost_uuid_uindex
	on lost_and_found (uuid);

create table lost_and_found
(
	item_id text not null,
	item_name text not null,
	lost_or_found boolean not null,
	user_id text not null,
	location text not null,
	description text,
	lf_time datetime not null,
	post_time datetime not null,
	image text,
	completed boolean not null,
	item_type text not null
);
