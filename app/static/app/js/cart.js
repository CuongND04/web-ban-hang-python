
// Bind event to Button Add to cart
const updateBtns = document.querySelectorAll(".update-cart")
for(i =0;i<updateBtns.length;i++){
  updateBtns[i].addEventListener('click',(e)=>{
    var productId = e.target.dataset.product
    var action =e.target. dataset.action
    // console.log(e.target.dataset.product)
    console.log(productId,action)
    console.log(user)
    if(user === "AnonymousUser"){
      console.log("not logged in")
    } else {
      updateUserOrder(productId,action)
    }
  })
}
// Hàm cập nhật đơn hàng
function updateUserOrder(productId,action){
  console.log("logged in")
  var url = '/update_item/'
  fetch(url,{
    method: 'POST',
    headers : {
      'Content-Type':'application/json',
      'X-CSRFTOKEN':csrftoken
    },
    body: JSON.stringify({"productId":productId,"action":action})
  })
  .then((res)=>res.json())
  .then(data =>{
    console.log(data)
  })
}