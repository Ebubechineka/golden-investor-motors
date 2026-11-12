# -*- coding: utf-8 -*-
"""Admin console: add / edit cars, stored in localStorage, exported as JSON."""
import os, sys, json
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
sys.path.insert(0,HERE)
import generate_site as G

ADMIN_JS = r"""
(function(){
  var KEY='gvm_admin_cars_v1';
  var BASE=window.__CARS__||[];
  function load(){
    try{ var raw=localStorage.getItem(KEY); if(!raw) return []; return JSON.parse(raw)||[]; }catch(e){ return []; }
  }
  function save(list){ try{ localStorage.setItem(KEY,JSON.stringify(list)); }catch(e){ alert('Could not save: browser storage is full or blocked.'); } }
  function all(){ return BASE.concat(load()); }
  function money(n){ return '\u20a6'+Number(n||0).toLocaleString('en-NG'); }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];}); }

  var tbody=document.getElementById('rows');
  var q=document.getElementById('q');
  var stat=document.getElementById('stat');

  function render(){
    var term=(q.value||'').trim().toLowerCase();
    var list=all().filter(function(c){
      if(!term) return true;
      return (c.brand+' '+c.model+' '+c.body+' '+c.fuel).toLowerCase().indexOf(term)>-1;
    });
    stat.textContent = term ? 'Filtered results' : 'Full catalogue';
    tbody.innerHTML=list.map(function(c){
      var custom=c.__custom?'<span class="badge badge-ok" style="font-size:.6rem">NEW</span>':'';
      return '<tr>'+
        '<td class="mono" style="font-size:.72rem">'+esc(c.id)+'</td>'+
        '<td><b>'+esc(c.brand)+'</b> '+esc(c.model)+' '+custom+'</td>'+
        '<td>'+esc(c.body)+'</td>'+
        '<td>'+esc(c.fuel)+'</td>'+
        '<td>'+esc(c.year)+'</td>'+
        '<td style="white-space:nowrap">'+money(c.price)+'</td>'+
        '<td style="white-space:nowrap">'+
          '<button class="btn btn-ghost btn-sm" data-edit="'+esc(c.id)+'">Edit</button> '+
          (c.__custom?'<button class="btn btn-dark btn-sm" data-del="'+esc(c.id)+'">Delete</button>':'')+
        '</td></tr>';
    }).join('') || '<tr><td colspan="7" style="text-align:center;padding:2rem;color:var(--text-dim)">No vehicles match.</td></tr>';
  }

  function findById(id){
    var b=BASE.filter(function(c){return c.id===id;})[0];
    if(b) return {car:b,custom:false};
    var l=load().filter(function(c){return c.id===id;})[0];
    return l?{car:l,custom:true}:null;
  }

  var form=document.getElementById('form');
  var fields=['id','brand','model','body','fuel','year','price','range_km','power_kw','battery_kwh','length','width','height','wheelbase','color','desc'];
  function fill(c){
    fields.forEach(function(f){
      var el=document.getElementById(f);
      if(!el) return;
      el.value=(c && c[f]!=null)?c[f]:'';
    });
    document.getElementById('formTitle').textContent=c?('Editing '+c.brand+' '+c.model):'Add a new vehicle';
    document.getElementById('cancelEdit').hidden=!c;
  }

  form.addEventListener('submit',function(ev){
    ev.preventDefault();
    var c={};
    fields.forEach(function(f){
      var el=document.getElementById(f);
      if(!el) return;
      var v=el.value.trim();
      if(['year','price','range_km','power_kw','battery_kwh','length','width','height','wheelbase'].indexOf(f)>-1){
        c[f]=v===''?null:Number(v);
      } else { c[f]=v; }
    });
    if(!c.brand||!c.model){ alert('Brand and model are required.'); return; }
    if(!c.id){
      c.id='cn-'+c.brand.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-'+c.model.toLowerCase().replace(/[^a-z0-9]+/g,'-');
    }
    c.__custom=true;
    var list=load();
    var idx=-1;
    for(var i=0;i<list.length;i++){ if(list[i].id===c.id){ idx=i; break; } }
    if(idx>-1){ list[idx]=c; } else { list.push(c); }
    save(list);
    fill(null); form.reset();
    render();
    document.getElementById('saved').hidden=false;
    setTimeout(function(){ document.getElementById('saved').hidden=true; },2500);
  });

  document.getElementById('cancelEdit').addEventListener('click',function(){ fill(null); form.reset(); });

  tbody.addEventListener('click',function(ev){
    var t=ev.target;
    if(t.dataset.edit){
      var r=findById(t.dataset.edit);
      if(r){ fill(r.car); window.scrollTo({top:0,behavior:'smooth'}); }
    }
    if(t.dataset.del){
      if(!confirm('Delete this vehicle from your local list?')) return;
      save(load().filter(function(c){return c.id!==t.dataset.del;}));
      render();
    }
  });

  q.addEventListener('input',render);

  document.getElementById('export').addEventListener('click',function(){
    var data=all().map(function(c){ var o={}; for(var k in c){ if(k!=='__custom') o[k]=c[k]; } return o; });
    var blob=new Blob([JSON.stringify(data,null,1)],{type:'application/json'});
    var a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download='catalog.json';
    a.click();
    setTimeout(function(){ URL.revokeObjectURL(a.href); },2000);
  });

  document.getElementById('resetLocal').addEventListener('click',function(){
    if(!confirm('Remove all vehicles you added in this browser? The built-in catalogue is not affected.')) return;
    localStorage.removeItem(KEY); render();
  });

  fill(null);
  render();
})();
"""

def build_admin():
    cars=G.CARS
    slim=[{k:c.get(k) for k in ('id','brand','model','body','fuel','year','price','range_km',
        'power_kw','battery_kwh','length','width','height','wheelbase','color','desc')} for c in cars]
    data=json.dumps(slim,ensure_ascii=False,separators=(',',':'))
    body=f"""
<section class="section" style="padding-bottom:1.5rem">
  <div class="wrap">
    <span class="eyebrow">Admin</span>
    <h1 class="display h1" style="font-size:clamp(2rem,4vw,3rem);margin-top:1rem">Vehicle console</h1>
    <p class="lede" style="margin-top:.9rem;max-width:70ch">Add a vehicle and its specs, or edit any car already in the catalogue. Changes are saved in this browser and appear in the table below immediately. Use <b>Export JSON</b> to download the full catalogue and publish it to the live site.</p>
    <div class="results-bar" style="margin-top:1.5rem;justify-content:flex-end">
      <div style="display:flex;gap:.6rem;flex-wrap:wrap">
        <button class="btn btn-gold btn-sm" id="export" type="button">Export JSON</button>
        <button class="btn btn-dark btn-sm" id="resetLocal" type="button">Clear my additions</button>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="admin-card">
      <h2 class="display" style="font-size:1.35rem" id="formTitle">Add a new vehicle</h2>
      <p class="muted" style="font-size:.85rem;margin-top:.4rem">Leave a spec blank if you do not have it — the page will simply omit it.</p>
      <form id="form" style="margin-top:1.5rem">
        <div class="admin-grid">
          <div class="field"><label for="brand">Brand *</label><input id="brand" required placeholder="e.g. BYD"></div>
          <div class="field"><label for="model">Model *</label><input id="model" required placeholder="e.g. Seal"></div>
          <div class="field"><label for="body">Body</label><input id="body" placeholder="SUV, Sedan, Hatchback…"></div>
          <div class="field"><label for="fuel">Fuel</label><input id="fuel" placeholder="Electric, Petrol, Plug-in Hybrid…"></div>
          <div class="field"><label for="year">Year</label><input id="year" type="number" min="1990" max="2030" placeholder="2026"></div>
          <div class="field"><label for="price">Price (₦)</label><input id="price" type="number" min="0" step="100000" placeholder="45000000"></div>
          <div class="field"><label for="range_km">Range (km)</label><input id="range_km" type="number" min="0" placeholder="570"></div>
          <div class="field"><label for="power_kw">Power (kW)</label><input id="power_kw" type="number" min="0" step="1" placeholder="390"></div>
          <div class="field"><label for="battery_kwh">Battery (kWh)</label><input id="battery_kwh" type="number" min="0" step="0.1" placeholder="82.5"></div>
          <div class="field"><label for="length">Length (mm)</label><input id="length" type="number" min="0" placeholder="4800"></div>
          <div class="field"><label for="width">Width (mm)</label><input id="width" type="number" min="0" placeholder="1875"></div>
          <div class="field"><label for="height">Height (mm)</label><input id="height" type="number" min="0" placeholder="1460"></div>
          <div class="field"><label for="wheelbase">Wheelbase (mm)</label><input id="wheelbase" type="number" min="0" placeholder="2920"></div>
          <div class="field"><label for="color">Colour</label><input id="color" placeholder="Obsidian Black"></div>
          <div class="field" style="grid-column:1/-1"><label for="desc">Description</label><textarea id="desc" rows="4" placeholder="Full description of the car…"></textarea></div>
          <div class="field" style="grid-column:1/-1"><label for="id">Stock ID (optional — auto-generated)</label><input id="id" placeholder="cn-byd-seal"></div>
        </div>
        <div style="display:flex;gap:.7rem;margin-top:1.5rem;flex-wrap:wrap;align-items:center">
          <button class="btn btn-gold" type="submit">Save vehicle</button>
          <button class="btn btn-ghost" type="button" id="cancelEdit" hidden>Cancel edit</button>
          <span id="saved" hidden style="color:var(--gold-400);font-size:.85rem">Saved to this browser.</span>
        </div>
      </form>
    </div>

    <div class="admin-card" style="margin-top:2rem">
      <div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:end">
        <h2 class="display" style="font-size:1.35rem">Catalogue</h2>
        <div style="display:flex;gap:1rem;align-items:end;flex-wrap:wrap">
          <p class="results-count" id="stat" style="padding-bottom:.7rem">—</p>
          <div class="field" style="min-width:240px"><label for="q">Search</label><input id="q" type="search" placeholder="Brand, model, body…"></div>
        </div>
      </div>
      <div class="admin-table-wrap">
        <table class="admin-table">
          <thead><tr><th>ID</th><th>Vehicle</th><th>Body</th><th>Fuel</th><th>Year</th><th>Price</th><th></th></tr></thead>
          <tbody id="rows"></tbody>
        </table>
      </div>
    </div>
  </div>
</section>
<script>window.__CARS__={data};</script>
<script>{ADMIN_JS}</script>
"""
    return G.head(f"Admin \u2014 {G.BRAND_UP}", "Vehicle console for Golden Investor Motors.",
                  "../") + G.header("../","") + body + G.footer("../")

def main():
    os.makedirs(os.path.join(ROOT,"admin"),exist_ok=True)
    with open(os.path.join(ROOT,"admin","index.html"),"w",encoding="utf-8") as f:
        f.write(build_admin())
    print("wrote admin/index.html")

if __name__=="__main__":
    main()
