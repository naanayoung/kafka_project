import React, { useState, useEffect } from 'react';
import axios from 'axios';
// useEffect : API 호출, useState : 받은 데이터의 상태 관리


function MyPage() {
	
	const [coupons, setCoupons] = useState([]);
	const token = localStorage.getItem('access'); // JWT 액세스 토큰 가져오기
	
	useEffect(() => {
		if (token) {
			// user_id를 통해 백엔드의 쿠폰 목록 GET 요청하기
			axios
				.get(`http://3.37.248.119:8000/api/coupon-list/`,{
					headers:{Authorization: `Bearer ${token}`,},
				})
			// 응답받은 데이터 coupons 에 저장
				.then((response) => {
					setCoupons(response.data);
				})
				.catch((error) => {
					console.error('쿠폰 조회 에러:', error);
				});
		}
	}, [token]);


	return (
		<div>
			<h2> My Coupon List </h2>
			{coupons.map((coupon) => (
				<div key={coupon.id}>
					<p>이벤트아이디 : {coupon.event_id}</p>
					<p>코드번호 : {coupon.code}</p>
					<p>발급일자 : {coupon.issued_at}</p>
					<p>사용여부 : {coupon.is_used}</p>
					<hr />
				</div>
			))}
		</div>
	);
}

export default MyPage;
