

CREATE TABLE app_user (
    user_id number GENERATED ALWAYS AS IDENTITY (START WITH 10 INCREMENT BY 10 NOCYCLE NOCACHE) PRIMARY KEY,
    username varchar2(1000),
    password varchar2(4000),
    role varchar2(500)
);


CREATE TABLE ticket (
    ticket_id number GENERATED ALWAYS AS IDENTITY (START WITH 100 INCREMENT BY 1 NOCYCLE NOCACHE),
    assigned_to number,
    submitted_by varchar2(2000),
    description varchar2(4000),
    created_at timestamp,
    started_at timestamp,
    finished_at timestamp,
    CONSTRAINT assigned_to_fk 
        FOREIGN KEY (assigned_to)
        REFERENCES app_user (user_id)
);