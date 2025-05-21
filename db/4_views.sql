-- files_summary
CREATE VIEW filestorage_files_summary as select file_id, category_name, type_name, file_fullway, file_fullway_test, file_fullway_nobaseway, file_fullway_forweb, filename as file_name, mime_type, mime_type_id, size_kb, html_video_ready, html_audio_ready, type_id, category_id, created_at from
(select *, 
concat(
  (select parameter_value FROM config where parameter_name = 'filemanager.baseway' and test_value), 
  way_category, way_type, way_file, filename
) as file_fullway_test,
concat(
  (select parameter_value FROM config where parameter_name = 'filemanager.baseway' and not test_value), 
  way_category, way_type, way_file, filename
) as file_fullway,
concat(
  way_category, way_type, way_file, filename
) as file_fullway_nobaseway,
concat(
  (select parameter_value FROM config where parameter_name = 'server.local_ip'), 
  (select parameter_value FROM config where parameter_name = 'filemanager.apache_storage_subdir'), 
  way_category, way_type, way_file, filename
) as file_fullway_forweb
from (select encode(id, 'hex') as file_id, type_id, way as way_file, filename, mime_type_id, size_kb, created_at from filestorage_files) ff 
left join (select id as type_id, category_id, type_name, way as way_type from filestorage_types where active = true) ft using(type_id)
left join (select id as category_id, category_name, way as way_category from filestorage_categories) fc using(category_id)
left join (select id as mime_type_id, type_name as mime_type, html_video_ready, html_audio_ready from mime_types_secondary) mts using(mime_type_id))
order by category_name asc, type_name asc, file_name asc;

-- mediafiles_summary
create view filestorage_mediafiles_summary as select * from (select * from filestorage_files_summary where mime_type like '%audio%' or mime_type like '%video%')
left join (select encode(file_id, 'hex') as file_id, duration as audio_duration, bitrate, sample_rate, artist, audio_title, album_title, "year", genre from filestorage_mediainfo_audio) fma using(file_id)
left join (select encode(file_id, 'hex') as file_id, duration as video_duration, fps, codec, width, height from filestorage_mediainfo_video) fmv using(file_id);

-- mimes_categories
create view filestorage_mimes_categories as 
select mime_type_id, count(mime_type_id) as mime_count, category_id from filestorage_files_summary fms 
group by mime_type_id, category_id order by category_id asc, mime_count desc;

-- -mimes_categories_summary
create view filestorage_mimes_categories_summary as 
select DISTINCT ON (category_id) category_id, mime_type_id from filestorage_mimes_categories;

-- mimes_types
create view filestorage_mimes_types as 
select mime_type_id, count(mime_type_id) as mime_count, type_id from filestorage_files_summary fms 
group by mime_type_id, type_id order by type_id asc, mime_count desc;

-- -mimes_types_summary
create view filestorage_mimes_types_summary as 
select DISTINCT ON (type_id) type_id, mime_type_id from filestorage_mimes_types; 