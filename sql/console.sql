
use class;
select distinct REGIONTYPE
from c_customer

select *
from c_customer

# null 데이터 존재할 가능성이 있어서 *로 진행

select concat(REGIONTYPE,' ',STATE) as area , count(*) as cnt
from c_customer
group by REGIONTYPE, STATE
having cnt > 100


select *
from c_product

select *
from c_order


select c.STATE, c.CITY, count(*) as order_cnt
from c_order o join c_customer c
    on o.CUSTOMERID = c.CUSTOMERID
group by c.STATE, c.CITY
order by 3 desc
;

select *
from(쿼리로 만든 데이터를 활용할 때 이 안에 집어 넣음) oc # 쿼리문을 데이터셋으로 활용하는 방법 : 인라인 뷰
;


select *
from c_order o join c_customer c
    on o.CUSTOMERID = c.CUSTOMERID

    join c_product p
    on o.PRODUCTID = p.PRODUCTID
limit 1


# new york 주 내의 도시별 총 주문금액과 주문건수를 내림차순으로 출력
# 주, 도시, 총 주문금액, 총 주문건수,
# 주문금액 내림차순 출력

select c.STATE, c.CITY, sum((p.PRICE*o.QUANTITY)-o.DISCOUNT), count(*)
from c_order o join c_customer c
    on o.CUSTOMERID = c.CUSTOMERID

    join c_product p
        on o.PRODUCTID = p.PRODUCTID
where c.STATE = 'New York'
group by c.CITY
order by sum(p.PRICE*o.QUANTITY-o.DISCOUNT) desc


use baemin;

# 지역별로 평점이 높은것부터 낮은순으로 출력
# 지역명, 평균평점, 총주문건수
select store_code, substr(store_addr,1,2) as area
from YogiyoFranchiseStore

select *
from YogiyoFranchiseReview

select substr(store_addr,1,2)
from YogiyoFranchiseStore s join YogiyoFranchiseReview r
on s.store_code = r.store_code
group by substr(store_addr,1,2)

create view yogiyo_avg_review_length as
select s.franchise_business, avg(length(r.review_content)) as avg_review_len
from YogiyoFranchiseStore s join YogiyoFranchiseReview r
on s.store_code = r.store_code
group by s.franchise_business

# view : 쿼리문 자체를 저장할 수 있어, 원본 데이터 접근 없이 공유 가능

select *
from BaeminFranchiseReview

select *
from BaeminFranchiseStore

# group by 함수시 기준들은 바로 기타함수 적용 가능, 나머지는 집계함수 이용
#1번 문제
select r.store_code, r.review_rating, count(review_answer_date)/count(*) as answer_rate
from BaeminFranchiseReview r join BaeminFranchiseStore s
on r.store_code = s.store_code
group by r.store_code, r.review_rating

#2번 문제
select r.store_code, count(review_answer_date)/count(*) as answer_rate
from BaeminFranchiseReview r join BaeminFranchiseStore s
on r.store_code = s.store_code
where r.review_rating = 3
group by r.store_code
order by count(review_answer_date)/count(*) desc

#3번 문제
select s.franchise_name, count(review_answer_date)/count(*) as answer_rate
from BaeminFranchiseReview r join BaeminFranchiseStore s
on r.store_code = s.store_code
where r.review_rating = 3
group by s.franchise_name
order by count(review_answer_date)/count(*) desc

# 2회차 강의
# select 사용시 alias를 꼭 앞에 붙여줘야함. (join 문)
# inner view 후에 join의 경우 최대한 inner view로 진행한 후 join을 진행해야 함
# index가 있어야 빨라짐 - B-tree 구조(cadinality 가 높을 수록[유니크한 값이 많다] 인덱 생성시 빨리 찾는다)
select ORDERDATE, c.CUSTOMERNAME, concat(STATE, ' ', CITy) as addr, p.PRODUCTNAME, p.PRICE
from (
        select *, row_number() over (partition by PRODUCTID order by ORDERDATE desc) as rn
        from c_order) a join c_customer c on a.CUSTOMERID = c.CUSTOMERID
                        join c_product p on a.PRODUCTID = p.PRODUCTID
where rn = 1
;

# 일자별 총 판매량

select substr(ORDERDATE, 1,10) as ymd, sum(QUANTITY) as total_order
from c_order
group by substr(ORDERDATE, 1,10)
order by substr(ORDERDATE, 1,10)

select *
from c_customer



# 첫 주문 이후 두번째 까지 1주일 이내인 고객명단을 구하라
# 남의 쿼리를 볼때 가장 안에 있는 쿼리부터 시작하여 살펴본다.
select CUSTOMERID, datediff(ORDERDATE, od_first) as datediff
from (select *, lag(ORDERDATE,1) over(partition by CUSTOMERID) as od_first
from (select CUSTOMERID, ORDERDATE, row_number() over (partition by CUSTOMERID order by ORDERDATE) as rn
      from c_order) s
where rn = 1 or rn = 2) ss
where rn = 2 and datediff(ORDERDATE, od_first) <=7


# 고객별 구매 제품 종류의 수
select *
from(select PRODUCTID
    from (select CUSTOMERID, count(distinct (PRODUCTID)) as od_pd_cnt
        from c_order
        group by CUSTOMERID
        order by count(distinct (PRODUCTID)) desc limit 1) s left outer join c_order
                                                           on s.CUSTOMERID = c_order.CUSTOMERID) ss
            join
          (select PRODUCTID, sum(QUANTITY)
            from c_order
            group by PRODUCTID
            order by sum(QUANTITY) desc) aa on ss.PRODUCTID = aa.PRODUCTID


select PRODUCTID, sum(QUANTITY)
from c_order
group by PRODUCTID
order by sum(QUANTITY) desc

# 복잡한 인라인 뷰의 작성시 덩어리를 먼저 생각하고 진행한다.