(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[405],{75557:function(e,t,a){(window.__NEXT_P=window.__NEXT_P||[]).push(["/",function(){return a(33760)}])},42449:function(e,t,a){"use strict";var o=a(28598),s=a(1887),r=a.n(s);let n=()=>(0,o.jsxs)(r(),{children:[(0,o.jsx)("title",{children:"Defog.ai - AI Assistant for Data Analysis"}),(0,o.jsx)("meta",{name:"description",content:"Train your AI data assistant on your own device"}),(0,o.jsx)("meta",{name:"viewport",content:"width=device-width, initial-scale=1"}),(0,o.jsx)("link",{rel:"icon",href:"/favicon.ico"})]});t.Z=n},22500:function(e,t,a){"use strict";var o=a(28598),s=a(82684),r=a(36189),n=a(79869),l=a(34376);a(12691);var i=a(26978),c=a(47663),u=a(56572);let d=e=>{let{id:t,userType:a,children:d,rootClassNames:f="",contentClassNames:g=""}=e,{Content:m,Sider:h}=n.Ar,[k,y]=(0,s.useState)([]),[x,w]=(0,s.useContext)(r.S),v=(0,l.useRouter)(),p=e=>{v.push(e)},j=()=>{localStorage.removeItem("defogUser"),localStorage.removeItem("defogToken"),localStorage.removeItem("defogUserType"),w({user:null,token:null,userType:null}),p("/log-in")},b=(0,c.usePathname)();(0,s.useEffect)(()=>{y(("admin"==a?[{key:"manage-database",title:"Manage Database",href:"/extract-metadata"},{key:"manage-users",title:"Manage Users",href:"/manage-users"},{key:"manage-tools",title:"Manage tools",href:"/manage-tools"},{key:"check-readiness",title:"Check Readiness",href:"/check-readiness"},{key:"align-model",title:"Align Model",href:"/align-model"},{key:"view-feedback",title:"View Feedback",href:"/view-feedback"},{key:"query-data",title:"Query Data",href:"/query-data"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:j}]:a?[{key:"view-notebooks",title:"View your notebook",href:"/view-notebooks"},{key:"query-data",title:"Query Data",href:"/query-data"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:j}]:[]).map(e=>(e.current=e.href==b,e)))},[a]);let[S,_]=(0,s.useState)("flex flex-col md:min-h-screen relative container mx-auto");return(0,s.useEffect)(()=>{"/query-data"===b&&_("flex flex-col md:min-h-screen relative")},[b]),(0,o.jsxs)("div",{className:(0,u.m6)(S,f),children:[k.length?(0,o.jsx)(i.l2,{rootClassNames:"border-b",items:k}):(0,o.jsx)(o.Fragment,{}),(0,o.jsx)("div",{className:(0,u.m6)("grow",g),children:d})]})};t.Z=d},33760:function(e,t,a){"use strict";a.r(t);var o=a(28598),s=a(82684),r=a(34376),n=a(42449),l=a(79869),i=a(36189),c=a(22500);let u=()=>{let[e,t]=(0,s.useState)(""),[a,u]=(0,s.useContext)(i.S),[d,f]=(0,s.useState)(!0),g=(0,r.useRouter)();return(0,s.useEffect)(()=>{let e=a.userType;if(!e){let o=localStorage.getItem("defogUser"),s=localStorage.getItem("defogToken");if(e=localStorage.getItem("defogUserType"),!o||!s||!e){g.push("/log-in");return}u({user:o,token:s,userType:e})}t(e),f(!1),"admin"===e?(console.log("redirecting to extract metadata.."),g.push("/extract-metadata")):(console.log("redirecting to view notebooks.."),g.push("/view-notebooks"))},[]),(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(n.Z,{}),(0,o.jsxs)(c.Z,{userType:e,children:[(0,o.jsx)("h1",{style:{paddingBottom:"1em"},children:"Welcome to Defog!"}),(0,o.jsxs)("h3",{children:["Please wait while we log you in and redirect you to the right page..."," ",(0,o.jsx)(l.yC,{})]})]})]})};t.default=u}},function(e){e.O(0,[435,774,888,179],function(){return e(e.s=75557)}),_N_E=e.O()}]);