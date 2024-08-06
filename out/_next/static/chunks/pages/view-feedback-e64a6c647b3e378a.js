(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[870],{86244:function(e,t,a){(window.__NEXT_P=window.__NEXT_P||[]).push(["/view-feedback",function(){return a(82473)}])},22295:function(e,t,a){"use strict";var n=a(28598),s=a(82684),o=a(33612),r=a(51728);t.Z=e=>{let{helperText:t,mainText:a,onUpdate:i,isEditable:l,inputModeOn:d=!1}=e,[c,u]=(0,s.useState)(a),[h,m]=(0,s.useState)(d),handleUpdate=()=>{i(c),m(!1)};return(0,n.jsxs)("div",{style:{backgroundColor:"#FFFAF0",borderLeft:"5px solid #FFA500",padding:"10px",margin:"10px 0",fontFamily:"Monospace",color:"#333",display:"flex",justifyContent:"space-between",alignItems:"center"},children:[(0,n.jsxs)("span",{children:[t,"\xa0"]}),h?(0,n.jsx)(o.default,{value:c,onChange:e=>u(e.target.value),onPressEnter:handleUpdate,onBlur:handleUpdate,autoFocus:!0,style:{flex:1}}):(0,n.jsx)("span",{style:{flex:1},children:c}),l&&(0,n.jsx)(r.default,{onClick:()=>m(!h),style:{cursor:"pointer",color:"#FFA500",marginLeft:"10px"}})]})}},26335:function(e,t,a){"use strict";var n=a(28598),s=a(1887),o=a.n(s);t.Z=()=>(0,n.jsxs)(o(),{children:[(0,n.jsx)("title",{children:"Defog.ai - AI Assistant for Data Analysis"}),(0,n.jsx)("meta",{name:"description",content:"Train your AI data assistant on your own device"}),(0,n.jsx)("meta",{name:"viewport",content:"width=device-width, initial-scale=1"}),(0,n.jsx)("link",{rel:"icon",href:"/favicon.ico"})]})},82067:function(e,t,a){"use strict";var n=a(28598),s=a(82684),o=a(97574),r=a(79869),i=a(34376);a(12691);var l=a(26978),d=a(47663),c=a(56572);t.Z=e=>{let{id:t,userType:a,children:u,rootClassNames:h="",contentClassNames:m=""}=e,{Content:f,Sider:p}=r.Layout,[g,y]=(0,s.useState)([]),[x,j]=(0,s.useContext)(o.S),k=(0,i.useRouter)(),redirect=e=>{k.push(e)},logout=()=>{localStorage.removeItem("defogUser"),localStorage.removeItem("defogToken"),localStorage.removeItem("defogUserType"),j({user:null,token:null,userType:null}),redirect("/static/log-in.html")},b=(0,d.usePathname)();(0,s.useEffect)(()=>{y(("admin"==a?[{key:"manage-database",title:"Manage Database",href:"/static/extract-metadata.html"},{key:"manage-users",title:"Manage Users",href:"/static/manage-users.html"},{key:"manage-tools",title:"Manage tools",href:"/static/manage-tools.html"},{key:"check-readiness",title:"Check Readiness",href:"/static/check-readiness.html"},{key:"align-model",title:"Align Model",href:"/static/align-model.html"},{key:"view-feedback",title:"View Feedback",href:"/static/view-feedback.html"},{key:"query-data",title:"Query Data",href:"/static/query-data.html"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:logout}]:a?[{key:"query-data",title:"Query Data",href:"/static/query-data.html"},{key:"logout",classNames:"self-end",title:"Logout",href:"#",onClick:logout}]:[]).map(e=>(e.current=e.href==b,e)))},[a]);let[w,v]=(0,s.useState)("flex flex-col md:min-h-screen relative container mx-auto");return(0,s.useEffect)(()=>{"/query-data"===b&&v("flex flex-col md:min-h-screen relative")},[b]),(0,n.jsxs)("div",{className:(0,c.m6)(w,h),children:[g.length?(0,n.jsx)(l.l2,{rootClassNames:"border-b",items:g}):(0,n.jsx)(n.Fragment,{}),(0,n.jsx)("div",{className:(0,c.m6)("grow",m),children:u})]})}},82473:function(e,t,a){"use strict";a.r(t),a.d(t,{default:function(){return view_feedback}});var n=a(28598),s=a(82684),o=a(26335),r=a(82067),i=a(79204),l=a(37490),d=a(92696),c=a(24788),u=a(33612),h=a(49603),m=a(10998),f=a(20259),p=a.n(f),g=a(18953),view_feedback_FeedbackTable=e=>{let{token:t,apiKeyName:a,feedbackColumns:o,feedback:r,filter:l,goldenQueries:d,setGoldenQueries:c,handleNegativeFeedback:u}=e,[f,y]=(0,s.useState)({}),[x,j]=(0,s.useState)(!1),[k,b]=(0,s.useState)(!1);(0,s.useEffect)(()=>{updateGoldenQueryMap()},[d,k,r]);let updateGoldenQueryMap=async()=>{let e={};r.forEach(t=>{let a="".concat(t[2],"_").concat(normalizeSQL(t[3])),n=(d||[]).some(e=>e.question===t[2]&&normalizeSQL(e.sql)===normalizeSQL(t[3]));e[a]=n}),y(e)},addToGoldenQueries=async(e,n)=>{let s=await checkifGoldenQuery(e,n);if(s)return;(d||[]).push({question:e,sql:n});let o=await fetch((0,i.Z)("http","integration/update_golden_queries"),{method:"POST",body:JSON.stringify({token:t,key_name:a,golden_queries:d}),headers:{"Content-Type":"application/json"}}),r=await o.json();return c(d),r},checkifGoldenQuery=async(e,t)=>{let a=(d||[]).some(a=>{let n=normalizeSQL(a.sql),s=normalizeSQL(t),o=a.question.trim()===e.trim();return o&&n===s});return a},handleAddToGoldenQueries=async(e,t)=>{j(!0);try{let a=await addToGoldenQueries(e,t);"success"==a.status&&g.default.success("Added to Golden Queries successfully!"),await updateGoldenQueryMap()}catch(e){console.error("Failed to add to golden queries:",e),g.default.error("Failed to add to Golden Queries.")}finally{j(!1),b(!k)}},normalizeSQL=e=>e.replace(/\s+/g," ").trim(),toFirstCapital=e=>e?e.charAt(0).toUpperCase()+e.slice(1).toLowerCase():e,w=o.map((e,t)=>"created_at"==e?{title:"Timestamp",dataIndex:e,key:e,render:e=>(0,n.jsx)("div",{style:{color:"grey"},children:new Date(e).toLocaleString("en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"})}),width:"7%",align:"center"}:"feedback_type"===e?{title:"Type",dataIndex:e,key:e,render:e=>(0,n.jsx)(p(),{type:"primary",shape:"round",size:"small",style:{backgroundColor:"bad"===e.toLowerCase()?"#f5222d":"#52c41a",borderColor:"bad"===e.toLowerCase()?"#f5222d":"#52c41a",color:"#fff"},children:toFirstCapital(e)}),width:"5%",align:"center"}:"query_generated"===e?{title:(0,n.jsx)("div",{style:{textAlign:"center"},children:"Generated SQL Query"}),dataIndex:e,key:e,render:e=>(0,n.jsx)("pre",{style:{whiteSpace:"pre-wrap",backgroundColor:"#f4f4f4",maxHeight:"300px",overflow:"auto"},children:e}),width:"40%"}:"feedback_text"===e?{title:"Feedback Text",dataIndex:e,key:e,render:e=>(0,n.jsx)("div",{style:{color:"#FF8C00",fontFamily:"Courier, monospace",fontSize:"1.1em",maxHeight:"300px",overflow:"auto"},children:e}),width:"20%",align:"center"}:"question"===e?{title:"Question",dataIndex:e,key:e,render:(e,t)=>(0,n.jsxs)("div",{style:{maxHeight:"300px",overflow:"auto"},children:[e,t.parentQuestionText&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("br",{}),(0,n.jsxs)("span",{style:{color:"grey"},children:["Parent Question Text: ",t.parentQuestionText]})]})]}),width:"20%",align:"center"}:{title:e,dataIndex:e,key:e});w.push({title:"Recommendation",key:"recommendation",render:(e,t)=>{let a=f["".concat(t.question,"_").concat(normalizeSQL(t.query_generated))];return"bad"===t.feedback_type.toLowerCase()?(0,n.jsx)(p(),{onClick:()=>u(t.question,t.query_generated,t.feedback_text),style:{backgroundColor:"#4CAF50",borderColor:"#4CAF50",color:"#fff",minWidth:"95%"},children:"Improve using Feedback"}):(0,n.jsx)(p(),{onClick:async()=>{try{await handleAddToGoldenQueries(t.question,t.query_generated)}catch(e){console.error("Failed to add to golden queries:",e)}},disabled:a,style:{backgroundColor:a?"#f0e68c":"#ffd700",borderColor:a?"#f0e68c":"#ffd700",color:"#000",opacity:a?.4:1,minWidth:"95%"},children:a?"Already a Golden Query":"Add to Golden Queries"})},width:"8%",align:"center"});let v=r.filter(e=>{var t,a,n;return(null===(t=e[1])||void 0===t?void 0:t.toLowerCase().includes(null==l?void 0:l.toLowerCase()))||(null===(a=e[2])||void 0===a?void 0:a.toLowerCase().includes(null==l?void 0:l.toLowerCase()))||(null===(n=e[3])||void 0===n?void 0:n.toLowerCase().includes(null==l?void 0:l.toLowerCase()))}),S=v.map((e,t)=>{let a={};return o.forEach((t,n)=>{a[t]=e[n]}),a.key=t,a});return(0,n.jsx)(h.default,{spinning:x,tip:"Adding to Golden Queries...",children:(0,n.jsx)("div",{className:"w-full h-full p-1 bg-gray-50 shadow rounded-lg",children:(0,n.jsx)(m.default,{columns:w,dataSource:S,pagination:!1,scroll:{x:!0},rowKey:"key"})})})},y=a(34376),DisplayDataFrame=function(e){let{columns:t,data:a}=e;return(0,n.jsxs)("table",{style:{width:"100%",borderCollapse:"collapse"},children:[(0,n.jsx)("thead",{children:(0,n.jsx)("tr",{children:t.map((e,t)=>(0,n.jsx)("th",{style:{border:"1px solid #ccc",padding:"8px",backgroundColor:"#eee"},children:e},t))})}),(0,n.jsx)("tbody",{children:a.map((e,t)=>(0,n.jsx)("tr",{children:e.map((e,t)=>(0,n.jsx)("td",{style:{border:"1px solid #ccc",padding:"8px"},children:e.toString()},t))},t))})]})},view_feedback_DisplayQuery=function(e){let{query:t}=e;return(0,n.jsx)("div",{style:{backgroundColor:"#f4f4f4",padding:"10px",borderRadius:"5px",fontFamily:"monospace"},children:(0,n.jsx)("pre",{children:t})})},x=a(22399),j=a(22295),k=a(70439),b=a(92e3),w=a(95153),v=a(20997),S=a(90353),_=a(80429),C=a(17931);let{TextArea:F}=u.default;var view_feedback_RecommendationsModal=e=>{let{isModalVisible:t,setIsModalVisible:a,token:o,apiKeyName:r,question:l,sqlGenerated:d,userFeedback:c,getCurrentGlossary:u}=e,m=(0,y.useRouter)(),[f,g]=(0,s.useState)(l),[T,Q]=(0,s.useState)(c),[G,N]=(0,s.useState)(""),[q,A]=(0,s.useState)(""),[L,I]=(0,s.useState)([]),[Z,E]=(0,s.useState)([]),[D,R]=(0,s.useState)(!0),[z,U]=(0,s.useState)(!1),[M,O]=(0,s.useState)(!1);(0,s.useEffect)(()=>{populateInstructions()},[T]);let closeModal=()=>{N(""),A(""),E([]),I([]),a(!1)},populateInstructions=async()=>{R(!0);try{let e=await fetch((0,i.Z)("http","get_instructions_recommendation"),{method:"POST",body:JSON.stringify({token:o,key_name:r,question:f,sql_generated:d,user_feedback:T}),headers:{"Content-Type":"application/json"}});if(!e.ok)throw Error("HTTP error, status = ".concat(e.status));let t=await e.json();if(t.error)throw Error(t.error);N(t.instruction_set||"")}catch(e){console.error("Failed to populate instructions:",e.message),N("Failed to load instructions due to an error.")}finally{R(!1)}},updateGlossary=async e=>{let t=await fetch((0,i.Z)("http","integration/update_glossary"),{method:"POST",body:JSON.stringify({token:o,key_name:r,glossary:e}),headers:{"Content-Type":"application/json"}}),a=await t.json();return a},reRunWithUpdatedInstructions=async()=>{U(!0);let e=await u(),t=e.concat(G),a=await fetch((0,i.Z)("http","query"),{method:"POST",body:JSON.stringify({token:o,key_name:r,question:f,previous_context:[],dev_body:!1,ignore_cache:!0,glossary:t}),headers:{"Content-Type":"application/json"}}),n=await a.json();A(n.query_generated),I(n.columns),E(n.data),U(!1),console.log(n)},permanentlyAddInstructions=async()=>{let e=await u(),t=e.concat("\n"+G);updateGlossary(t),N(""),O(!0)};return(0,n.jsx)(x.default,{title:"",open:t,onOk:closeModal,onCancel:closeModal,width:"80vw",children:(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)("div",{children:[(0,n.jsx)("h2",{style:{textAlign:"center",marginTop:"1em",marginBottom:"1em"},children:(0,n.jsxs)("div",{children:[(0,n.jsx)(k.Z,{className:"text-4xl"}),(0,n.jsx)("p",{className:"text-2xl mt-4",children:"Recommendations"})]})}),(0,n.jsx)(j.Z,{helperText:(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(_.Z,{style:{fontSize:"16px",color:"##FFFAF0"}}),"\xa0 Your Feedback:"]}),mainText:c,onUpdate:e=>{Q(e)},isEditable:!D}),(0,n.jsx)("p",{style:{paddingLeft:"1.1em"},children:D?"The more meaningful the feedback, the better suggestions you get! You will soon have an option to edit the feedback and doing so automatically regenerates new instructions for you!":"Based on your feedback these are the instructions when given to the model might help get the right answer. Feel free to edit before hitting ask defog again:"}),D?(0,n.jsx)(h.default,{tip:"Aligning the model based on your feedback. This might take up to 30-60 seconds. We appreciate your patience!",children:(0,n.jsx)(F,{disabled:!0,placeholder:"Generating instructions...",style:{width:"95%",padding:"1em",margin:"1em"}})}):(0,n.jsx)(F,{value:G,onChange:e=>{N(e.target.value)},placeholder:"Instructions Appear Here",style:{width:"95%",padding:"1em",margin:"1em",minHeight:"150px"}})]}),(0,n.jsx)(j.Z,{helperText:(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(C.default,{style:{fontSize:"16px",color:"##FFFAF0"}}),"\xa0 Question:"]}),mainText:l,onUpdate:e=>g(e),isEditable:!D&&!z}),(0,n.jsx)("div",{children:(0,n.jsxs)(p(),{onClick:reRunWithUpdatedInstructions,type:"dashed",style:{minWidth:"23%",padding:"1.2em",paddingBottom:"1.1em",margin:"1em",marginBottom:"0.5em",marginTop:"0.5em",height:"auto"},disabled:""===G||D||z,children:[(0,n.jsx)(w.Z,{style:{fontSize:"20px",marginRight:"8px"}}),z?"Running...":"Ask Defog with Updated Instructions"]})}),!D&&q&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)("div",{style:{width:"95%",paddingLeft:"1.1em"},children:[(0,n.jsxs)("h2",{className:"text-xl mt-4 mb-3",style:{textAlign:"left"},children:[" ",(0,n.jsx)(b.Z,{style:{fontSize:"24px",marginRight:"8px"}})," ","Updated Results Using Instructions"]}),(0,n.jsx)("h3",{className:"text-lg mt-2 mb-1 text-left",children:"Generated SQL Query"}),(0,n.jsx)(view_feedback_DisplayQuery,{query:q}),(0,n.jsx)("h3",{className:"text-lg mt-2 mb-1 text-left",children:"Query Results"}),(0,n.jsx)(DisplayDataFrame,{columns:L,data:(Z||[]).map(e=>e.map(e=>e))})]}),(0,n.jsxs)("div",{children:[(0,n.jsx)(j.Z,{helperText:(0,n.jsx)(S.Z,{style:{fontSize:"16px",color:"##FFFAF0"}}),mainText:"Did this improve your results? If yes, consider adding those instructions to the glossary permanently to tailor it for the future.",onUpdate:()=>{},isEditable:!1}),(0,n.jsxs)(p(),{onClick:permanentlyAddInstructions,type:"dashed",style:{minWidth:"23%",padding:"1.2em",paddingBottom:"1.2em",margin:"1em",marginBottom:"0.5em",marginTop:"0.5em",height:"auto"},children:[(0,n.jsx)(v.Z,{style:{fontSize:"20px",marginRight:"8px"}}),"Add Recommendations to Glossary"]}),M&&(0,n.jsxs)("p",{style:{paddingLeft:"1em",marginTop:"1em"},children:["Instructions have been added to ","",(0,n.jsx)("span",{style:{cursor:"pointer",color:"#1890ff",textDecoration:"underline",fontWeight:"bold"},onClick:()=>m.push("/align-model"),children:"glossary"})," ","successfully."]})]})]})]})})},T=a(94242),view_feedback=()=>{let e="Defog".split(","),[t,a]=(0,s.useState)(null),[m,f]=(0,s.useState)(),[p,g]=(0,s.useState)([]),[y,x]=(0,s.useState)([]),[j,k]=(0,s.useState)([]),[b,w]=(0,s.useState)(""),[v,S]=(0,s.useState)(""),[_,C]=(0,s.useState)(""),[F,Q]=(0,s.useState)(!1),[G,N]=(0,s.useState)(""),[q,A]=(0,s.useState)(!1);(0,s.useEffect)(()=>{let t=localStorage.getItem("defogDbSelected"),n=localStorage.getItem("defogToken");t?a(t):a(e[0]),f(n)},[]),(0,s.useEffect)(()=>{t&&localStorage.setItem("defogDbSelected",t),getFeedback(m,t),getGoldenQueries()},[m,t]);let getFeedback=async(e,t)=>{if(A(!0),!e)return;let a=await fetch((0,i.Z)("http","get_feedback"),{method:"POST",body:JSON.stringify({token:e,key_name:t}),headers:{"Content-Type":"application/json"}}),n=await a.json();g(n.columns),x(n.data),A(!1)},fetchCurrentGlossaryAndGoldenQueries=async(e,t)=>{let a=await fetch((0,i.Z)("http","integration/get_glossary_golden_queries"),{method:"POST",body:JSON.stringify({token:e,key_name:t}),headers:{"Content-Type":"application/json"}}),n=await a.json();return{glossary:n.glossary||"",goldenQueries:n.golden_queries||""}},getCurrentGlossary=async()=>{if(!m||!t)return;let{glossary:e}=await fetchCurrentGlossaryAndGoldenQueries(m,t);return e},getGoldenQueries=async()=>{if(!m||!t)return;let{goldenQueries:e}=await fetchCurrentGlossaryAndGoldenQueries(m,t);k(e)},handleNegativeFeedback=async(e,t,a)=>{w(e),S(t),C(a),Q(!0)};return(0,n.jsxs)("div",{className:"flex justify-center",children:[(0,n.jsx)(o.Z,{}),(0,n.jsxs)(r.Z,{id:"view-feedback",userType:"admin",children:[e.length>1?(0,n.jsx)(l.default,{type:"flex",height:"100vh",children:(0,n.jsx)(d.default,{span:24,style:{paddingBottom:"1em"},children:(0,n.jsx)(c.default,{style:{width:"100%"},onChange:e=>{a(e)},options:e.map(e=>({value:e,key:e,label:e})),value:t})})}):null,(0,n.jsxs)("div",{className:"w-full",children:[(0,n.jsxs)("div",{className:"flex justify-center items-center flex-col m-3",children:[(0,n.jsxs)("h1",{children:[(0,n.jsx)(T.Z,{style:{fontSize:"3em",color:"#1890ff"}})," "]}),(0,n.jsx)("h1",{className:"text-2xl mt-4",children:"Feedback History"})]}),(0,n.jsx)(l.default,{className:"flex justify-center mb-4",children:(0,n.jsx)(d.default,{span:24,children:(0,n.jsx)(u.default,{placeholder:"Filter rows by text",onChange:e=>{N(e.target.value)},className:"w-full p-3 rounded-lg border border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 transition duration-200"})})}),(0,n.jsx)(h.default,{spinning:q,tip:"Loading past feedback data...",children:(0,n.jsx)(view_feedback_FeedbackTable,{token:m,apiKeyName:t,feedbackColumns:p,feedback:y,filter:G,goldenQueries:j,setGoldenQueries:k,handleNegativeFeedback:handleNegativeFeedback})}),F&&(0,n.jsx)(view_feedback_RecommendationsModal,{isModalVisible:F,setIsModalVisible:Q,token:m,apiKeyName:t,question:b,sqlGenerated:v,userFeedback:_,getCurrentGlossary:getCurrentGlossary})]})]})]})}},79204:function(e,t){"use strict";t.Z=(e,t)=>{if("http"!==e&&"ws"!==e)throw Error("Protocol not supported");return(console.log("http://localhost:33364"),""!==t)?"ws"===e?"".concat("http://localhost:33364".replace("http","ws"),"/").concat(t):"".concat("http://localhost:33364","/").concat(t):"".concat("http://localhost:33364")}}},function(e){e.O(0,[435,209,774,888,179],function(){return e(e.s=86244)}),_N_E=e.O()}]);