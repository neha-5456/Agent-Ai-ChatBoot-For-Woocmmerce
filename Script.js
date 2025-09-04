<!-- wp:pattern {"slug":"twentytwentyfour/footer"} /-->
<script>
    (function(){
      function el(tag, cls, html){var e=document.createElement(tag); if(cls) e.className=cls; if(html) e.innerHTML=html; return e}
      var container=document.createElement('div'); container.style.position='fixed'; container.style.bottom='20px'; container.style.left='20px'; container.style.zIndex='99999';
      var toggle=el('div','',"🤖"); 
      toggle.style.cssText="width:50px;height:50px;border-radius:50%;background:#ff6a00;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:24px;";
      container.appendChild(toggle);
    
      var panel=el('div',''); 
      panel.style.cssText="display:none;background:#fff;border-radius:8px;padding:14px;width:300px;box-shadow:0 2px 8px rgba(0,0,0,.2);";
      panel.innerHTML="<div>👋 Hi! I'm your shopping assistant. How can I help?</div>";
    
      var btns=el('div','');
      ["Check My Order","Browse Products","Get Discount","Other Questions"].forEach(function(label){
        var b=el('button','',label);
        b.style.cssText="display:block;width:100%;margin:6px 0;padding:8px;background:#ff6a00;color:#fff;border:none;border-radius:6px;cursor:pointer;";
        b.onclick=function(){
          var intent;
          if(label.includes("Order")) intent="check_order";
          else if(label.includes("Browse")) intent="browse_products";
          else if(label.includes("Discount")) intent="get_discount";
          else intent="other";
          var query="";
          if(intent==="check_order") query=prompt("Enter your order ID or email:");
          else if(intent==="other") query=prompt("Type your question:");
          fetch("http://127.0.0.1:8000/api/chatbot/chat/", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({intent:intent, query:query})
          })
          .then(r=>r.json()).then(j=>{ alert("Bot: " + j.reply); });
        };
        btns.appendChild(b);
      });
      panel.appendChild(btns);
      container.appendChild(panel);
      toggle.onclick=function(){ panel.style.display= panel.style.display==="none"?"block":"none"; };
      document.body.appendChild(container);
    })();
    </script>
    