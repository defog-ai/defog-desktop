(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[405],{75557:function(e,t,a){(window.__NEXT_P=window.__NEXT_P||[]).push(["/",function(){return a(48591)}])},26335:function(e,t,a){"use strict";var s=a(28598),l=a(1887),r=a.n(l);t.Z=()=>(0,s.jsxs)(r(),{children:[(0,s.jsx)("title",{children:"Defog.ai - AI Assistant for Data Analysis"}),(0,s.jsx)("meta",{name:"description",content:"Train your AI data assistant on your own device"}),(0,s.jsx)("meta",{name:"viewport",content:"width=device-width, initial-scale=1"}),(0,s.jsx)("link",{rel:"icon",href:"/favicon.ico"})]})},82067:function(e,t,a){"use strict";var s=a(28598),l=a(82684),r=a(97574),o=a(79869),i=a(34376);a(12691);var n=a(26978),c=a(47663),u=a(56572);t.Z=e=>{let{id:t,userType:a,children:d,rootClassNames:m="",contentClassNames:h=""}=e,{Content:g,Sider:f}=o.Layout,[x,y]=(0,l.useState)([]),[k,p]=(0,l.useContext)(r.S),w=(0,i.useRouter)(),redirect=e=>{w.push(e)},logout=()=>{localStorage.removeItem("defogUser"),localStorage.removeItem("defogToken"),localStorage.removeItem("defogUserType"),p({user:null,token:null,userType:null}),redirect("/static/log-in.html")},v=(0,c.usePathname)();(0,l.useEffect)(()=>{y(("admin"==a?[{key:"manage-database",title:"Manage Database",href:"/static/extract-metadata.html"},{key:"manage-users",title:"Manage Users",href:"/static/manage-users.html"},{key:"manage-tools",title:"Manage tools",href:"/static/manage-tools.html"},{key:"check-readiness",title:"Check Readiness",href:"/static/check-readiness.html"},{key:"align-model",title:"Align Model",href:"/static/align-model.html"},{key:"view-feedback",title:"View Feedback",href:"/static/view-feedback.html"},{key:"query-data",title:"Query Data",href:"/static/query-data.html"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:logout}]:a?[{key:"query-data",title:"Query Data",href:"/static/query-data.html"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:logout}]:[]).map(e=>(e.current=e.href==v,e)))},[a]);let[j,N]=(0,l.useState)("flex flex-col md:min-h-screen relative container mx-auto");return(0,l.useEffect)(()=>{"/query-data"===v&&N("flex flex-col md:min-h-screen relative")},[v]),(0,s.jsxs)("div",{className:(0,u.m6)(j,m),children:[x.length?(0,s.jsx)(n.l2,{rootClassNames:"border-b",items:x}):(0,s.jsx)(s.Fragment,{}),(0,s.jsx)("div",{className:(0,u.m6)("grow",h),children:d})]})}},48591:function(e,t,a){"use strict";a.r(t);var s=a(28598),l=a(82684),r=a(34376),o=a(26335),i=a(97574),n=a(82067),c=a(49603);t.default=()=>{let[e,t]=(0,l.useState)(""),[a,u]=(0,l.useContext)(i.S),[d,m]=(0,l.useState)(!0),h=(0,r.useRouter)();return(0,l.useEffect)(()=>{let e=a.userType;if(!e){let t=localStorage.getItem("defogUser"),a=localStorage.getItem("defogToken");if(e=localStorage.getItem("defogUserType"),!t||!a||!e){h.push("/log-in");return}u({user:t,token:a,userType:e})}t(e),m(!1),"admin"===e?(console.log("redirecting to extract metadata.."),h.push("/static/extract-metadata.html")):(console.log("redirecting to query data.."),h.push("/static/query-data.html"))},[]),(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.Z,{}),(0,s.jsx)(n.Z,{userType:e,children:(0,s.jsx)("div",{className:"flex flex-col items-center justify-center min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8",children:(0,s.jsxs)("div",{className:"max-w-md w-full space-y-8 p-10 bg-white rounded-xl shadow-md",children:[(0,s.jsxs)("div",{className:"text-center",children:[(0,s.jsx)("h1",{className:"text-3xl font-semibold text-gray-900 mb-4",children:"Welcome to Defog!"}),(0,s.jsxs)("h3",{className:"text-lg text-gray-700",children:["Please wait while we log you in and redirect you to the right page... ",(0,s.jsx)(c.default,{})]})]}),d&&(0,s.jsx)("div",{className:"flex justify-center mt-6",children:(0,s.jsxs)("svg",{className:"animate-spin h-5 w-5 text-indigo-600",xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",children:[(0,s.jsx)("circle",{className:"opacity-25",cx:"12",cy:"12",r:"10",stroke:"currentColor",strokeWidth:"4"}),(0,s.jsx)("path",{className:"opacity-75",fill:"currentColor",d:"M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"})]})})]})})})]})}}},function(e){e.O(0,[435,774,888,179],function(){return e(e.s=75557)}),_N_E=e.O()}]);