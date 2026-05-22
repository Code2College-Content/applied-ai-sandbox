(() => {
  const notes = window.INITIAL_NOTES || [];
  const q = document.getElementById('q');
  const resultsEl = document.getElementById('results');
  const clearBtn = document.getElementById('clear');
  const countEl = document.getElementById('count');
  const noteEl = document.getElementById('note');
  const noteEmpty = document.getElementById('note-empty');
  const noteTitle = document.getElementById('note-title');
  const noteTags = document.getElementById('note-tags');
  const noteBody = document.getElementById('note-body');

  let activeId = null;

  function renderList(list, query) {
    resultsEl.innerHTML = '';
    list.forEach(n => {
      const li = document.createElement('li');
      li.className = 'result-item';
      li.dataset.id = n.id;
      const title = document.createElement('div');
      title.className = 'result-title';
      title.innerHTML = highlight(n.title, query);
      const meta = document.createElement('div');
      meta.className = 'result-meta mono';
      meta.textContent = `ID: ${n.id}`;
      li.appendChild(title);
      li.appendChild(meta);
      li.addEventListener('click', () => selectNote(n.id));
      if (n.id === activeId) li.classList.add('active');
      resultsEl.appendChild(li);
    });
    countEl.textContent = `${list.length} result${list.length===1?'':'s'}${query?` for '${query}'`:''}`;
  }

  function highlight(text, q) {
    if (!q) return escapeHtml(text);
    const re = new RegExp(`(${escapeRegExp(q)})`, 'ig');
    return escapeHtml(text).replace(re, '<mark>$1</mark>');
  }

  function escapeHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
  function escapeRegExp(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}

  function selectNote(id){
    activeId = id;
    const note = notes.find(n=>n.id===id);
    if(!note) return;
    noteEmpty.style.display = 'none';
    noteEl.classList.remove('hidden');
    noteTitle.textContent = note.title;
    noteTags.textContent = (note.tags && note.tags.length)? note.tags.join(', ') : '';
    noteBody.textContent = note.body;
    // update active class
    Array.from(resultsEl.children).forEach(li => li.classList.toggle('active', Number(li.dataset.id)===id));
  }

  function filter(qs){
    qs = (qs||"").trim();
    if(!qs) return notes.slice();
    const lowered = qs.toLowerCase();
    return notes.filter(n => (n.title||'').toLowerCase().includes(lowered));
  }

  function onInput(){
    const val = q.value;
    clearBtn.classList.toggle('show', !!val);
    const items = filter(val);
    renderList(items, val);
    if(items.length && activeId==null){
      selectNote(items[0].id);
    }
  }

  q && q.addEventListener('input', debounce(onInput, 150));
  clearBtn && clearBtn.addEventListener('click', (e)=>{e.preventDefault(); q.value=''; q.focus(); onInput();});

  // initial render
  renderList(notes, '');

  function debounce(fn, wait){let t;return (...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),wait);};}

})();
