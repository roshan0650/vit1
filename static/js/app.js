function $(q){return document.querySelector(q)}
function $all(q){return document.querySelectorAll(q)}

$all('.option').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const id = btn.getAttribute('data-target');
    const el = document.getElementById(id);
    if(el){ el.classList.add('show'); }
  })
})

$all('.close-modal').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const id = btn.getAttribute('data-target');
    const el = document.getElementById(id);
    if(el){ el.classList.remove('show'); }
  })
})

function goBack(){ window.history.back(); }

function countWords(text){
  return (text.trim().match(/\S+/g) || []).length;
}

function validateReviewLength(textareaId, maxWords){
  const el = document.getElementById(textareaId);
  if(!el) return true;
  const words = countWords(el.value);
  if(words > maxWords){
    alert(`Please limit your review to ${maxWords} words. Current: ${words}`);
    return false;
  }
  return true;
}
