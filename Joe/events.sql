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

create table events
(
	uuid text not null,
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

item_id = str(input("Enter item id:"))
    user_id = str(input("Enter user id:"))
    title = str(input("Enter title:"))
    image = str(input("Enter image:"))
    description = str(input("Enter description:"))
    deadline = input("Enter deadline:")
    activity_time = input("Enter activity time:")
    location = str(input("Enter location:"))
    activity_type = str(input("Enter activity type:"))
    space_used = input("Enter space used:")
    space_limit = input("Enter space limit:")