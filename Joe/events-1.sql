create table events
(
	uuid text not null
		constraint explore_pk
			primary key,
	user_id text not null,
	title text not null,
	image text,
	description text,
	post_time datetime not null,
	deadline datetime not null,
	activity_time datetime,
	location text,
	activity_type text,
	space_used int,
	space_limit int 
);

create unique index explore_uuid_uindex
	on events (uuid);

