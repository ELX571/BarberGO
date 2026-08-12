// Minimal interactivity + API integration
const API_BASE = window.API_BASE || '';

document.getElementById('menuBtn')?.addEventListener('click', function(){
  const nav = document.getElementById('navList');
  if(!nav) return;
  nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
});

async function handleForm(e){
  e.preventDefault();
  const form = e.target;
  const data = {
    name: form.name.value,
    contact: form.contact.value,
    message: form.message.value
  };

  try{
    const res = await fetch(API_BASE + '/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if(!res.ok){
      const text = await res.text().catch(()=>res.statusText);
      throw new Error(text || 'Server error');
    }

    alert('Rahmat, ' + (data.name || "do\'st") + '! Sizning xabaringiz qabul qilindi.');
    form.reset();
  }catch(err){
    // Inform user the frontend reached the backend but it failed, or network error occurred.
    alert('Xabar yuborilmadi — backend muammosi yoki tarmoq xatosi: ' + (err.message || err));
    console.error('Contact submit error:', err);
  }
}

async function loadServices(){
  const grid = document.getElementById('servicesGrid');
  if(!grid) return;
  try{
    const res = await fetch(API_BASE + '/services');
    if(!res.ok) throw new Error('no services');
    const items = await res.json();
    if(!Array.isArray(items)) throw new Error('invalid response');

    grid.innerHTML = '';
    for(const it of items){
      const article = document.createElement('article');
      article.className = 'card';
      article.innerHTML = `<h3>${escapeHtml(it.title || '')}</h3><p>${escapeHtml(it.description || '')}</p>`;
      grid.appendChild(article);
    }
  }catch(err){
    // Keep static fallback; log error for dev
    console.warn('Could not load services from API:', err);
  }
}

function escapeHtml(s){
  return String(s)
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'","&#39;");
}

window.handleForm = handleForm;

// Try to load dynamic services on start
loadServices();
