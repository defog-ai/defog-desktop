(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[720],{13831:function(e,t,o){(window.__NEXT_P=window.__NEXT_P||[]).push(["/log-in",function(){return o(88357)}])},26335:function(e,t,o){"use strict";var l=o(28598),n=o(1887),r=o.n(n);t.Z=()=>(0,l.jsxs)(r(),{children:[(0,l.jsx)("title",{children:"Defog.ai - AI Assistant for Data Analysis"}),(0,l.jsx)("meta",{name:"description",content:"Train your AI data assistant on your own device"}),(0,l.jsx)("meta",{name:"viewport",content:"width=device-width, initial-scale=1"}),(0,l.jsx)("link",{rel:"icon",href:"/favicon.ico"})]})},82067:function(e,t,o){"use strict";var l=o(28598),n=o(82684),r=o(97574),a=o(79869),s=o(34376);o(12691);var i=o(26978),u=o(47663),c=o(56572);t.Z=e=>{let{id:t,userType:o,children:d,rootClassNames:h="",contentClassNames:g=""}=e,{Content:m,Sider:f}=a.Layout,[v,p]=(0,n.useState)([]),[y,w]=(0,n.useContext)(r.S),x=(0,s.useRouter)(),redirect=e=>{x.push(e)},logout=()=>{localStorage.removeItem("defogUser"),localStorage.removeItem("defogToken"),localStorage.removeItem("defogUserType"),w({user:null,token:null,userType:null}),redirect("/static/log-in.html")},k=(0,u.usePathname)();(0,n.useEffect)(()=>{p(("admin"==o?[{key:"manage-database",title:"Manage Database",href:"/static/extract-metadata.html"},{key:"manage-users",title:"Manage Users",href:"/static/manage-users.html"},{key:"manage-tools",title:"Manage tools",href:"/static/manage-tools.html"},{key:"check-readiness",title:"Check Readiness",href:"/static/check-readiness.html"},{key:"align-model",title:"Align Model",href:"/static/align-model.html"},{key:"view-feedback",title:"View Feedback",href:"/static/view-feedback.html"},{key:"query-data",title:"Query Data",href:"/static/query-data.html"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:logout}]:o?[{key:"query-data",title:"Query Data",href:"/static/query-data.html"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:logout}]:[]).map(e=>(e.current=e.href==k,e)))},[o]);let[_,j]=(0,n.useState)("flex flex-col md:min-h-screen relative container mx-auto");return(0,n.useEffect)(()=>{"/query-data"===k&&j("flex flex-col md:min-h-screen relative")},[k]),(0,l.jsxs)("div",{className:(0,c.m6)(_,h),children:[v.length?(0,l.jsx)(i.l2,{rootClassNames:"border-b",items:v}):(0,l.jsx)(l.Fragment,{}),(0,l.jsx)("div",{className:(0,c.m6)("grow",g),children:d})]})}},88357:function(e,t,o){"use strict";o.r(t),o.d(t,{default:function(){return log_in}});var l=o(28598),n=o(82684),r=o(34376),a=o(26335),s=o(33612),i=o(85439),u=o(20259),c=o.n(u),d=o(18953),h=o(97574),g=o(82067);let m=(0,n.createContext)(null);function GoogleOAuthProvider({clientId:e,nonce:t,onScriptLoadSuccess:o,onScriptLoadError:l,children:r}){let a=function(e={}){let{nonce:t,onScriptLoadSuccess:o,onScriptLoadError:l}=e,[r,a]=(0,n.useState)(!1),s=(0,n.useRef)(o);s.current=o;let i=(0,n.useRef)(l);return i.current=l,(0,n.useEffect)(()=>{let e=document.createElement("script");return e.src="https://accounts.google.com/gsi/client",e.async=!0,e.defer=!0,e.nonce=t,e.onload=()=>{var e;a(!0),null===(e=s.current)||void 0===e||e.call(s)},e.onerror=()=>{var e;a(!1),null===(e=i.current)||void 0===e||e.call(i)},document.body.appendChild(e),()=>{document.body.removeChild(e)}},[t]),r}({nonce:t,onScriptLoadSuccess:o,onScriptLoadError:l}),s=(0,n.useMemo)(()=>({clientId:e,scriptLoadedSuccessfully:a}),[e,a]);return n.createElement(m.Provider,{value:s},r)}let f={large:40,medium:32,small:20};function GoogleLogin({onSuccess:e,onError:t,useOneTap:o,promptMomentNotification:l,type:r="standard",theme:a="outline",size:s="large",text:i,shape:u,logo_alignment:c,width:d,locale:h,click_listener:g,containerProps:v,...p}){let y=(0,n.useRef)(null),{clientId:w,scriptLoadedSuccessfully:x}=function(){let e=(0,n.useContext)(m);if(!e)throw Error("Google OAuth components must be used within GoogleOAuthProvider");return e}(),k=(0,n.useRef)(e);k.current=e;let _=(0,n.useRef)(t);_.current=t;let j=(0,n.useRef)(l);return j.current=l,(0,n.useEffect)(()=>{var e,t,l,n,m,f,v,I,S;if(x)return null===(l=null===(t=null===(e=null==window?void 0:window.google)||void 0===e?void 0:e.accounts)||void 0===t?void 0:t.id)||void 0===l||l.initialize({client_id:w,callback:e=>{var t;if(!(null==e?void 0:e.credential))return null===(t=_.current)||void 0===t?void 0:t.call(_);let{credential:o,select_by:l}=e;k.current({credential:o,clientId:function(e){var t;let o=null!==(t=null==e?void 0:e.clientId)&&void 0!==t?t:null==e?void 0:e.client_id;return o}(e),select_by:l})},...p}),null===(f=null===(m=null===(n=null==window?void 0:window.google)||void 0===n?void 0:n.accounts)||void 0===m?void 0:m.id)||void 0===f||f.renderButton(y.current,{type:r,theme:a,size:s,text:i,shape:u,logo_alignment:c,width:d,locale:h,click_listener:g}),o&&(null===(S=null===(I=null===(v=null==window?void 0:window.google)||void 0===v?void 0:v.accounts)||void 0===I?void 0:I.id)||void 0===S||S.prompt(j.current)),()=>{var e,t,l;o&&(null===(l=null===(t=null===(e=null==window?void 0:window.google)||void 0===e?void 0:e.accounts)||void 0===t?void 0:t.id)||void 0===l||l.cancel())}},[w,x,o,r,a,s,i,u,c,d,h]),n.createElement("div",{...v,ref:y,style:{height:f[s],...null==v?void 0:v.style}})}var v=o(63509),p=o(79204),y=o(48497);let w=y.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID||"REPLACE_WITH_GOOGLE_CLIENT_ID";var auth_GoogleLogin=()=>{let[e,t]=(0,n.useContext)(h.S),o=(0,r.useRouter)(),onSuccess=async e=>{console.log("Login Success: ",e);let l=await fetch((0,p.Z)("http","login_google"),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({credential:e.credential})});if(l.ok){let e=await l.json();e.error&&(console.error(e.error),d.default.error(e.error)),"success"===e.status&&(t({user:e.user_email,token:e.token,userType:e.user_type}),localStorage.setItem("defogUser",e.user_email),localStorage.setItem("defogToken",e.token),localStorage.setItem("defogUserType",e.user_type),o.push("/"))}};return(0,l.jsx)("div",{children:(0,l.jsx)(GoogleOAuthProvider,{clientId:w,children:(0,l.jsx)(GoogleLogin,{buttonText:"Log In with Google",onSuccess:onSuccess,onFailure:e=>{console.error("Login Failed: ",e),v.default},cookiePolicy:"single_host_origin"})})})},log_in=()=>{let[e,t]=(0,n.useContext)(h.S),o=(0,r.useRouter)(),handleLogin=async e=>{let l=await fetch("http://localhost:33364/login",{method:"POST",body:JSON.stringify(e)}),n=await l.json();"success"===n.status?(t({user:e.username,token:n.token,userType:n.user_type}),localStorage.setItem("defogUser",e.username),localStorage.setItem("defogToken",n.token),localStorage.setItem("defogUserType",n.user_type),o.push("/static/extract-metadata.html")):d.default.error("Login failed. Please contact your administrator.")};return(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)(a.Z,{}),(0,l.jsxs)(g.Z,{children:[(0,l.jsx)("h1",{style:{paddingBottom:"1em"},children:"Welcome to Defog!"}),(0,l.jsxs)(i.default,{labelCol:{span:4},wrapperCol:{span:20},style:{maxWidth:800},onFinish:handleLogin,children:[(0,l.jsx)(i.default.Item,{label:"Username",name:"username",children:(0,l.jsx)(s.default,{})}),(0,l.jsx)(i.default.Item,{label:"Password",name:"password",children:(0,l.jsx)(s.default.Password,{})}),(0,l.jsx)(i.default.Item,{children:(0,l.jsx)(c(),{type:"primary",htmlType:"submit",children:"Log In"})})]}),(0,l.jsx)(auth_GoogleLogin,{})]})]})}},79204:function(e,t){"use strict";t.Z=(e,t)=>{if("http"!==e&&"ws"!==e)throw Error("Protocol not supported");return(console.log("http://localhost:33364"),""!==t)?"ws"===e?"".concat("http://localhost:33364".replace("http","ws"),"/").concat(t):"".concat("http://localhost:33364","/").concat(t):"".concat("http://localhost:33364")}}},function(e){e.O(0,[435,774,888,179],function(){return e(e.s=13831)}),_N_E=e.O()}]);