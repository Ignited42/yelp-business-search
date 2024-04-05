UPDATE business
SET Total_checkin = (SELECT sum(*) FROM CheckinLogs.Checkin_count WHERE CheckinLogs.Business_id = Business.Business_id),
    Num_review = (SELECT count(*) FROM Review WHERE Review.Business_id = Business.Business_id),
    Business_rating = (SELECT avg(*) FROM Review.Rating WHERE Review.Business_id = Business.Business_id);