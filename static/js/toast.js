function showToast(title, msg, type='info') {
  const wrap = document.querySelector('#toastStack');
  if (!wrap) return;
  
  const div = document.createElement('div');
  const color = type === 'error' 
    ? 'bg-red-500' 
    : type === 'success' 
      ? 'bg-green-500' 
      : 'bg-blue-500';
      
  div.className = `${color} text-white px-4 py-3 rounded-lg shadow flex items-center justify-between animate-fade-in-down`;
  div.innerHTML = `<div><b>${title}</b><br>${msg}</div>`;
  
  wrap.appendChild(div);
  setTimeout(() => div.remove(), 3000);
}
