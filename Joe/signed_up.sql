create table signed_up
(
	uuid text not null
		constraint signed_up_pk
			primary key,
	user_email text not null,
	user_name text not null,
	signup_time datetime not null,
	gender text,
	picture text,
	follower int,
	following int

);

create unique index signed_up_uuid_uindex
	on signed_up (uuid);

