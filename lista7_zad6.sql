select * from dbo.rates;

select top(1000) * from dbo.Facts;

select top(1000) F.ProductID, R.date, F.TimeID, R.rates, F.TotalDue, R.rates * F.TotalDue as pln_value
from dbo.rates as R
inner join dbo.Facts as F
on R.date = F.TimeID;

UPDATE dbo.Facts 
set pln_value = R.rates * F.TotalDue
from dbo.rates as R
inner join dbo.Facts as F
on R.date = F.TimeID;


