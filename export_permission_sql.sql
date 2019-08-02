select 
'access_' || replace(m.model, '.', '_') as id, 
 m.model as name, 
'oemedical.model_' || replace(m.model, '.', '_') as "model_id:id",
d.name as "group_id:id",
cast(a.perm_read as int) as perm_read, 
cast(a.perm_write as int) as perm_write,
cast(a.perm_create as int) as perm_create, 
cast(a.perm_unlink as int) as perm_unlink
from ir_model_access a 
inner join ir_model m on a.model_id = m.id 
inner join res_groups g  on a.group_id = g.id
inner join ir_model_data d on d.res_id = a.group_id and d.model = 'res.groups'
where a.group_id = 22


--select * from ir_model_data d where d.model = 'res.partner' and d.res_id = 

select * from ir_model_data dd where dd.model = 'res.partner' 
--and dd.res_id = 61  limit 1