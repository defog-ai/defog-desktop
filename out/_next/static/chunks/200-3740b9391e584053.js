"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[200],{86447:function(e,t,a){a.d(t,{Bl:function(){return setChartJSDefaults},EY:function(){return cleanString},Iq:function(){return getColValues},LS:function(){return reFormatData},Mf:function(){return _},XA:function(){return processData},o$:function(){return createChartConfig},qz:function(){return roundColumns},xb:function(){return isEmpty}}),a(82684);var n=a(79555),r=a.n(n),o=a(25943),l=a.n(o),i=a(98242),s=a.n(i),u=a(60524),c=a.n(u),d=a(89486),m=a.n(d),p=a(89921),f=a(44333);r().extend(c()),r().extend(s()),r().extend(l()),r().extend(m());let g=["YYYY-MM-DD HH:mm:ss","YYYY-MM-DDTHH:mm:ss","YYYY-MM-DD","YYYY-MM","YYYY-MMM"];function cleanString(e){return String(e).toLowerCase().replace(/ /gi,"-")}function roundColumns(e,t){let a=null==t?void 0:t.filter(e=>"decimal"===e.colType).map(e=>e.key),n=[];return null==e||e.forEach((e,t)=>{n.push(Object.assign({},e)),null==a||a.forEach(e=>{let a=n[t][e];try{Math.abs(a)>.01?n[t][e]=Math.round(100*a)/100:n[t][e]=Math.round(1e6*a)/1e6}catch(r){console.log(r),n[t][e]=a}})}),n}function isNumber(e){let t=/\d%?$/.test(e);return/^-?(0|[1-9]\d*)?(\.\d+)?%?$/.test(e)&&t}function formatTime(e){e=e.replace(/\w\S*/g,function(e){return e.charAt(0).toUpperCase()+e.substr(1).toLowerCase()});let t=r()(e,g,!0);return t.isValid()?t.format("D MMM 'YY"):e}function setChartJSDefaults(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"",a=arguments.length>2&&void 0!==arguments[2]&&arguments[2],n=arguments.length>3?arguments[3]:void 0,r=arguments.length>4&&void 0!==arguments[4]&&arguments[4];e.defaults.scale.grid.drawOnChartArea=!1,e.defaults.interaction.axis="x",e.defaults.interaction.mode="nearest",e.defaults.maintainAspectRatio=!1,e.defaults.plugins.title.display=!0,r||(e.defaults.plugins.title.text=t),e.defaults.plugins.tooltip.backgroundColor="white",e.defaults.plugins.tooltip.titleColor="#0D0D0D",e.defaults.plugins.tooltip.bodyColor="#0D0D0D",e.defaults.plugins.tooltip.borderColor="#2B59FF",e.defaults.plugins.tooltip.borderWidth=1,e.defaults.plugins.tooltip.padding=10,e.defaults.plugins.title.color=null==n?void 0:n.primaryText,e.defaults.plugins.tooltip.displayColors=!1,e.defaults.plugins.tooltip.callbacks.title=function(e){return e.map(e=>a?formatTime(e.label):e.label)},e.defaults.scales.category.ticks={callback:function(e){return a?formatTime(this.getLabelForValue(e)):this.getLabelForValue(e)}},e.defaults.plugins.tooltip.callbacks.label=function(e){return e.dataset.label+": "+e.formattedValue},r&&(e.overrides.pie.plugins.legend.labels.filter=function(e){return e.text=a?formatTime(e.text):e.text,!0})}function getColValues(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[];if(!t.length||!e||!e.length)return[];let a=new Set;return e.forEach(e=>{let n=t.reduce((t,a,n)=>(n>0&&(t+="-"),t+=e[a]),"");a.add(n)}),Array.from(a)}function processData(e,t){let a=null==t?void 0:t.filter(e=>"date"===e.colType),n=null==t?void 0:t.filter(e=>{var t;return(null==e?void 0:null===(t=e.variableType)||void 0===t?void 0:t[0])==="c"&&"date"!==e.colType}),r=null==t?void 0:t.filter(e=>{var t;return(null==e?void 0:null===(t=e.variableType)||void 0===t?void 0:t[0])!=="c"&&"date"!==e.colType}),o=null==t?void 0:t.slice(),l={};null==o||o.forEach(t=>{l[t.key]=getColValues(e,[t.key])});let i=sanitiseData(e,!0);return{xAxisColumns:o||[],categoricalColumns:n||[],yAxisColumns:r||[],dateColumns:a||[],xAxisColumnValues:l,data:i}}function isEmpty(e){for(let t in e)if(Object.hasOwn(e,t))return!1;return!0}function sanitiseData(e){let t,a=arguments.length>1&&void 0!==arguments[1]&&arguments[1];return Array.isArray(e)&&e?(a?(t=e).forEach(e=>{Object.entries(e).forEach(t=>{let[a,n]=t;"string"==typeof n&&n.endsWith("%")&&(e[a]=+n.slice(0,-1))})}):t=e.filter(e=>e).filter(e=>!e.every(e=>null===e)),t):[]}function createChartConfig(e,t,a,n,r){if(!t.length||!a.length||!n||!e||!e.length)return{chartLabels:[],chartData:[]};let o=null==n?void 0:n.map(e=>e.label),l=e.filter(e=>{let a=getColValues([e],t.map(e=>e.label))[0];return e.__xLab__=a,null==o?void 0:o.includes(a)});if(l=l.reduce((e,t)=>{let n=t.__xLab__;return e[n]||(e[n]={},a.forEach(t=>{e[n][t.label]=0})),a.forEach(a=>{e[n][a.label]+=t[a.label]}),e},{}),r){let e=t[0].__data__,a=(null==e?void 0:e.dateToUnix)||(e=>e);o.sort((e,t)=>a(e)-a(t))}else null==o||o.sort((e,t)=>l[t][a[0].label]-l[e][a[0].label]);l=Object.entries(l).map(e=>{let[t,n]=e,r={__xLab__:t};return a.forEach(e=>{r[e.label]=n[e.label]}),r}),r&&l.sort((e,t)=>{if(r)return o.indexOf(e.__xLab__)-o.indexOf(t.__xLab__)});let i=null==a?void 0:a.map((e,t)=>({label:e.label,data:l,backgroundColor:p.vK[t%p.vK.length],parsing:{xAxisKey:"__xLab__",yAxisKey:e.label,key:e.label}}));return{chartData:i,chartLabels:o}}let reFormatData=(e,t)=>{let a,n;let o=[],l=[],i=sanitiseData(e,!1);if(function(e){if(!Array.isArray(e)||!e)return[];let t=e.map(e=>String(e));return t}(t).length&&i.length){a=[],n=[];for(let e=0;e<t.length;e++){let n=function(e,t,a){let n={};if(n.numeric=!1,n.variableType="quantitative",a.endsWith("_id")||a.startsWith("id_")||"id"===a)return n.colType="string",n.variableType="categorical",n.numeric=!1,n.simpleTypeOf="string",n;for(let o=0;o<e.length;o++){let l=e[o][t];if(null===l)continue;let i=function(e,t,a,n){let o,l,i=r()(e,g,!0).isValid()||/^year$/gi.test(a)||/^month$/gi.test(a)||/^date$/gi.test(a)||/^week$/gi.test(a)||/year/gi.test(a)||/month/gi.test(a)||/date/gi.test(a)||/week/gi.test(a),dateToUnix=e=>e;if(i){if((/^year$/gi.test(a)||/year/gi.test(a))&&(o="year"),(/^month$/gi.test(a)||/month/gi.test(a))&&(o="month"),(/^date$/gi.test(a)||/date/gi.test(a))&&(o="date"),(/^week$/gi.test(a)||/week/gi.test(a))&&(o="week"),"week"===o&&(dateToUnix=e=>r()().week(+e).unix(),l="W-YYYY"),"year"===o&&(dateToUnix=e=>r()("1-"+ +e,"M-YYYY").unix(),l="M-YYYY"),"month"===o)for(let e=0;e<n.length;e++){let a=n[e][t];if(a){if("number"==typeof a)dateToUnix=e=>r()(e+"-"+new Date().getFullYear(),"M-YYYY").unix(),l="M-YYYY";else{let e=/[a-zA-Z]/.test(a);e?a.length>3?(dateToUnix=e=>r()(e,"MMMM").unix(),l="MMMM"):(dateToUnix=e=>r()(e,"MMM").unix(),l="MMM"):(dateToUnix=e=>r()(e+"-"+new Date().getFullYear(),"M-YYYY").unix(),l="M-YYYY")}break}}"date"===o&&(dateToUnix=e=>r()(e).unix(),l=null)}else dateToUnix=e=>e,l=null,o=null,i=!1;return{isDate:i,dateType:o,parseFormat:l,dateToUnix}}(l,t,a,e);if(i.isDate)n.colType="date",n.variableType="categorical",n.numeric=!1,n.parseFormat=i.parseFormat,n.dateToUnix=i.dateToUnix,n.dateType=i.dateType,n.isDate=i.isDate;else if(isNumber(l)&&l.toString().indexOf(".")>=0){n.colType="decimal",n.numeric=!0,n.variableType="quantitative";try{n.mean=(0,f.Z)(e,e=>e[t])}catch(e){}}else if(isNumber(l)||/^-?(0|[1-9]\d*)?(\.\d+)?([eE][-+]?\d+)?$/.test(l))n.colType="integer",n.numeric=!0,n.variableType="quantitative",n.mean=(0,f.Z)(e,e=>e[t]);else if(n.colType=typeof l,n.numeric="number"===n.colType,n.variableType="number"===n.colType?"quantitative":"categorical",n.numeric)try{n.mean=(0,f.Z)(e,e=>e[t])}catch(e){}return n.simpleTypeOf=typeof l,n}}(i,e,t[e]),s=Object.assign({title:t[e],dataIndex:t[e],key:t[e],simpleTypeOf:typeof i[0][e],sorter:i.length>0&&"number"==typeof i[0][e]?(a,n)=>a[t[e]]-n[t[e]]:i.length>0&&!isNaN(i[0][e])?(a,n)=>Number(a[t[e]])-Number(n[t[e]]):(a,n)=>String(a[t[e]]).localeCompare(String(n[t[e]])),render:e=>"number"!=typeof e&&isNaN(e)?e:n.isDate?e:Number(e).toLocaleString(),...n});a.push(s),a[e].numeric&&"string"===a[e].simpleTypeOf&&o.push(e),a[e].numeric&&"number"===a[e].simpleTypeOf&&"categorical"===a[e].variableType&&l.push(e)}for(let e=0;e<i.length;e++){let a={};a.key=e,a.index=e;for(let n=0;n<t.length;n++)o.indexOf(n)>=0?a[t[n]]=i[e][n]:l.indexOf(n)>=0?a[t[n]]=""+i[e][n]:a[t[n]]=i[e][n];n.push(a)}a.push({title:"index",dataIndex:"index",key:"index",sorter:(e,t)=>e.index-t.index,colType:"integer",variableType:"integer",numeric:!0,simpleTypeOf:"number",mean:((null==n?void 0:n.length)+1)/2||null})}else a=[],n=[];return{newCols:a,newRows:n}},_={kmc:"Kaplan-Meier Curves",boxplot:"Boxplot",heatmap:"Heatmap"}},89921:function(e,t,a){a.d(t,{Ni:function(){return r},de:function(){return o},vK:function(){return l}}),a(28598);var n=a(82684);let r=(0,n.createContext)({}),o={primaryText:"#0D0D0D",secondaryText:"#161616",brandColor:"#2B59FF",background1:"#FFFFFF",background2:"#F8FAFB",background3:"#F8FAFB",disabledColor:"#f5f5f5",greyBorder:"#EFF1F5",questionBorder:"#EFF1F5",answerBorder:"#EFF1F5"},l=["#D52D68","#540CC9","#2B59FF","#FFB536","#3EE0D5","#561981"]},60516:function(e,t,a){a.d(t,{z:function(){return Button}});var n=a(28598),r=a(56572);let Button=e=>{let{onClick:t=()=>{},className:a="",children:o=null,disabled:l=!1}=e;return(0,n.jsx)("button",{disabled:l,onClick:e=>{l||t(e)},className:(0,r.m6)("px-2 py-1 rounded-md text-white bg-blue-500 text-xs hover:bg-blue-600",l?"cursor-not-allowed bg-gray-100 text-gray-400 hover:bg-gray-100":"",a),children:o})}},5237:function(e,t,a){a.d(t,{Z:function(){return SingleSelect}});var n=a(28598),r=a(33662),o=a(56106),l=a(78725),i=a(52897),s=a(82684),u=a(56572);function SingleSelect(e){let{rootClassName:t="",popupClassName:a="",onChange:c=null,defaultValue:d=null,options:m=[],label:p=null}=e,[f,g]=(0,s.useState)(""),_=""===f?m:m.filter(e=>(console.log(e),(e.label+"").toLowerCase().includes(f.toLowerCase()))),[h,y]=(0,s.useState)(m.find(e=>e.value===d));return(0,n.jsxs)(r.hQ,{as:"div",by:"value",className:t,value:h,defaultValue:d,onChange:e=>{g(""),y(e),e&&c&&"function"==typeof c&&c(e)},children:[p&&(0,n.jsx)(o.__,{className:"block text-sm mb-2 font-medium leading-6 text-gray-900",children:"Assigned to"}),(0,n.jsxs)("div",{className:"relative",children:[(0,n.jsx)(r.gA,{className:"w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-blue-400 sm:text-sm sm:leading-6",onChange:e=>g(e.target.value),onBlur:()=>g(""),displayValue:e=>null==e?void 0:e.label}),(0,n.jsx)(r.Q$,{className:"absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none",children:(0,n.jsx)(l.Z,{className:"h-5 w-5 text-gray-400","aria-hidden":"true"})}),_.length>0&&(0,n.jsx)(r.L5,{className:(0,u.m6)("z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm absolute bottom-10",a),children:_.map(e=>(0,n.jsx)(r.O2,{value:e,className:e=>{let{focus:t}=e;return(0,u.m6)("relative cursor-default select-none py-2 pl-3 pr-9",t?"bg-blue-400 text-white":"text-gray-900")},children:t=>{let{focus:a,selected:r}=t;return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("span",{className:(0,u.m6)("block truncate",r&&"font-semibold"),children:e.label}),r&&(0,n.jsx)("span",{className:(0,u.m6)("absolute inset-y-0 right-0 flex items-center pr-4",a?"text-white":"text-blue-400"),children:(0,n.jsx)(i.Z,{className:"h-5 w-5","aria-hidden":"true"})})]})}},e.value))})]})]})}},30972:function(e,t,a){a.d(t,{Z:function(){return Table}});var n=a(28598),r=a(82684),o=a(56572),l=a(5237),i=a(85692),s=a(25473);let u=[10,20,50,100],defaultSorter=(e,t)=>String(e).localeCompare(String(t));function Table(e){let{columns:t,rows:a,rootClassName:c="",pagination:d={defaultPageSize:10,showSizeChanger:!0},skipColumns:m=[]}=e,[p,f]=(0,r.useState)(1),[g,_]=(0,r.useState)(d.defaultPageSize),h=(0,r.useMemo)(()=>t.filter(e=>!m.includes(e.dataIndex)),[t,m]),[y,b]=(0,r.useState)(null),[x,v]=(0,r.useState)(null),[w,T]=(0,r.useState)(a),D=h.map(e=>e.dataIndex),C=Math.ceil(a.length/g);function toggleSort(e,t){(null==y?void 0:y.title)===(null==e?void 0:e.title)&&x===t?(b(null),v(null)):(b(e),v(t))}return(0,r.useEffect)(()=>{if(y&&x){let e=y.sorter||defaultSorter,t=a.slice().sort((t,a)=>"asc"===x?e(t,a):e(a,t));T(t)}else T(a)},[y,a,x]),(0,n.jsxs)("div",{className:(0,o.m6)("overflow-auto",c),children:[(0,n.jsx)("div",{className:"overflow-auto",children:(0,n.jsx)("div",{className:"py-2",children:(0,n.jsxs)("table",{className:"divide-y w-full divide-gray-300",children:[(0,n.jsx)("thead",{className:"bg-gray-50",children:(0,n.jsx)("tr",{children:h.map((e,t)=>(0,n.jsx)("th",{scope:"col",className:(0,o.m6)(0===t?"pl-4":"px-3","py-3.5 text-left text-sm font-semibold text-gray-900",t===h.length-1?"pr-4 sm:pr-6 lg:pr-8":""),children:(0,n.jsxs)("div",{className:"flex flex-row items-center",children:[(0,n.jsx)("p",{className:"grow",children:e.title}),(0,n.jsxs)("div",{className:"sorter-arrows ml-5 flex flex-col items-center w-4 overflow-hidden",children:[(0,n.jsx)("button",{className:"h-3",children:(0,n.jsx)("div",{onClick:()=>{toggleSort(e,"asc")},className:(0,o.m6)("arrow-up cursor-pointer","border-b-[5px] border-b-gray-300 hover:border-b-gray-500","asc"===x&&y.title===e.title?"border-b-gray-500":"")})}),(0,n.jsx)("button",{className:"h-3",children:(0,n.jsx)("div",{onClick:()=>{toggleSort(e,"desc")},className:(0,o.m6)("arrow-down cursor-pointer","border-t-[5px] border-t-gray-300 hover:border-t-gray-500","desc"===x&&y.title===e.title?"border-t-gray-500":"")})})]})]})},e.key))})}),(0,n.jsx)("tbody",{className:"divide-y divide-gray-200 bg-white",children:w.slice((p-1)*g,p*g).map(e=>(0,n.jsx)("tr",{children:D.map((t,a)=>(0,n.jsx)("td",{className:(0,o.m6)(0===a?"pl-4":"px-3","py-4 text-sm text-gray-500",a===D.length-1?"pr-4 sm:pr-6 lg:pr-8":""),children:e[t]},e.key+"-"+t))},e.key))})]})})}),(0,n.jsx)("div",{className:"pl-4 pager mt-3 text-center bg-white",children:(0,n.jsxs)("div",{className:"w-full flex flex-row justify-end items-center",children:[(0,n.jsxs)("div",{className:"flex flex-row w-50 items-center",children:[(0,n.jsxs)("div",{className:"text-gray-600",children:["Page",(0,n.jsx)("span",{className:"mx-1 font-semibold",children:p}),"/",(0,n.jsx)("span",{className:"mx-1 font-semibold",children:C})]}),(0,n.jsx)(i.Z,{className:(0,o.m6)("w-5 cursor-not-allowed",1===p?"text-gray-300":"hover:text-blue-500 cursor-pointer"),onClick:()=>{f(p-1<1?1:p-1)}}),(0,n.jsx)(s.Z,{className:(0,o.m6)("w-5 cursor-pointer",p===C?"text-gray-300 cursor-not-allowed":"hover:text-blue-500 cursor-pointer"),onClick:()=>{f(p+1>C?C:p+1)}})]}),(0,n.jsx)("div",{className:"w-full flex",children:(0,n.jsx)(l.Z,{rootClassName:"w-24",options:u.map(e=>({value:e,label:e})),defaultValue:g,onChange:e=>_(e.value)})})]})})]})}},89199:function(e,t,a){a.d(t,{LK:function(){return addTool},Q1:function(){return c},Ov:function(){return arrayOfObjectsToObject},TN:function(){return createAnalysis},t8:function(){return createInitialToolInputs},oe:function(){return deleteDoc},Uj:function(){return deleteToolRunIds},SV:function(){return p},Xp:function(){return getAllAnalyses},df:function(){return u},UU:function(){return getAllDocs},ny:function(){return getAnalysis},c8:function(){return getCursorColor},WJ:function(){return getTableData},Cy:function(){return getToolRunData},tD:function(){return getToolboxes},le:function(){return isNullOrUndefined},IR:function(){return parseData},QV:function(){return roundNumber},c2:function(){return d},BP:function(){return m},JM:function(){return f}});var n=a(78259),r=a(79204),o=a(72497);let l={data_fetcher_and_aggregator:{name:"data_fetcher_and_aggregator",function_name:"Fetch data from database",description:"Converting a natural language question into a SQL query, that then runs on an external database. Fetches, filters, aggregates, and performs arithmetic computations on data. Remember that this tool does not have access to the data returned by the previous steps. It only has access to the data in the database.",input_metadata:{question:{name:"question",default:null,description:"natural language description of the data required to answer this question (or get the required information for subsequent steps) as a string",type:"str"}},toolbox:"data_fetching",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},global_dict_data_fetcher_and_aggregator:{name:"global_dict_data_fetcher_and_aggregator",function_name:"Query data from a pandas dataframe",description:"Converting a natural language question into a SQL query, that then runs on a database that is stored in global_dict. Fetches, filters, aggregates, and performs arithmetic computations on data. This tool has access to all of global_dict. This will only run on the data that is stored in global_dict. For external databases, use the data_fetcher_and_aggregator tool.",input_metadata:{question:{name:"question",default:null,description:"natural language description of the data required as a string",type:"str"},input_df:{name:"input_df",default:null,meta_:"global_dict.<input_df_name>",description:"The dataframe to query",type:"pandas.core.frame.DataFrame"}},toolbox:"data_fetching",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},t_test:{name:"t_test",function_name:"T Test",description:"This function gets two groups and runs a t-test to check if there is a significant difference between their means. There are two ways to run the test: paired and unpaired. Paired test has one group column, unpaired has one group column.",input_metadata:{full_data:{name:"full_data",default:null,description:"input_df_name",type:"pandas.core.frame.DataFrame"},group_column:{name:"group_column",default:null,description:"group column",type:"DBColumn"},score_column:{name:"score_column",default:null,description:"score column",type:"DBColumn"},name_column:{name:"name_column",default:null,description:"name column or None",type:"DBColumn"},t_test_type:{name:"t_test_type",default:["unpaired","paired"],description:"type of t test as a string (paired or unpaired)",type:"DropdownSingleSelect"}},toolbox:"stats",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},fold_change:{name:"fold_change",function_name:"Fold Change",description:"This function calculates the fold change over time for different groups. Fold change is the ratio of the final value to the initial value.",input_metadata:{full_data:{name:"full_data",default:null,description:"input_df_name",type:"pandas.core.frame.DataFrame"},value_column:{name:"value_column",default:null,description:"value column (the numerical value)",type:"DBColumn"},individual_id_column:{name:"individual_id_column",default:null,description:"individual id column (the column that represents individual ids to calculate fold change for)",type:"DBColumn"},time_column:{name:"time_column",default:null,description:"time column (the column that represents the time point)",type:"DBColumn"},group_column:{name:"group_column",default:null,description:"group column or None (the column that represents the groups that individuals belong to, like cohort or study)",type:"DBColumn"}},toolbox:"stats",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},anova_test:{name:"anova_test",function_name:"ANOVA Test",description:"This function gets more than two groups and runs an anova test to check if there is a significant difference between their means.",input_metadata:{full_data:{name:"full_data",default:null,description:"input_df_name",type:"pandas.core.frame.DataFrame"},group_column:{name:"group_column",default:null,description:"group column",type:"DBColumn"},score_column:{name:"score_column",default:null,description:"score column",type:"DBColumn"}},toolbox:"stats",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},wilcoxon_test:{name:"wilcoxon_test",function_name:"Wilcoxon Test",description:"This function gets two groups and runs a wilcoxon test to check if there is a significant difference between their means.",input_metadata:{full_data:{name:"full_data",default:null,description:"input_df_name",type:"pandas.core.frame.DataFrame"},group_column:{name:"group_column",default:null,description:"group column",type:"DBColumn"},score_column:{name:"score_column",default:null,description:"score column",type:"DBColumn"},name_column:{name:"name_column",default:null,description:" name column",type:"DBColumn"}},toolbox:"stats",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},line_plot:{name:"line_plot",function_name:"Line Plot",description:"This function generates a line plot using python's seaborn library. It should be used when the user wants to see how a variable changes over time, and should be used immediately after the data_fetcher tool.",input_metadata:{full_data:{name:"full_data",default:null,description:"input_df_name",type:"pandas.core.frame.DataFrame"},x_column:{name:"x_column",default:null,description:"(exactly a single column - often a datetime or string)",type:"DBColumn"},y_column:{name:"y_column",default:null,description:"(exactly a single column - always a numerical value)",type:"DBColumn"},hue_column:{name:"hue_column",default:null,description:"column name to use for hue or None",type:"DBColumn"},facet_col:{name:"facet_col",default:null,description:"column name to use for faceting or None",type:"DBColumn"},estimator:{name:"estimator",default:["mean","median","max","min","sum","None"],description:'"mean" if data must be aggregated, "None" if it is not aggregated',type:"DropdownSingleSelect"},units:{name:"units",default:null,description:"column name or None - refers to the column that contains individual data points, often some kind of id",type:"DBColumn"},plot_average_line:{name:"plot_average_line",default:["False","True"],description:"True if the user wants to plot an average or median line",type:"DropdownSingleSelect"},average_type:{name:"average_type",default:["mean","median","max","min","mode"],description:"the kind of value for the average line to have. Can be mean, median, max, min, or mode. None if no average line required",type:"DropdownSingleSelect"}},toolbox:"plots",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},boxplot:{name:"boxplot",function_name:"Boxplot",description:"Generates a boxplot using python's seaborn library. Also accepts a faceting column. This usually required the full dataset and not summary statistics. Use the facet feature only when specifically asked for it.",input_metadata:{full_data:{name:"full_data",default:null,description:"input_df_name",type:"pandas.core.frame.DataFrame"},boxplot_cols:{name:"boxplot_cols",default:null,description:"Array of boxplot x column and boxplot y column",type:"DBColumnList_1_2"},facet:{name:"facet",default:!1,description:"True if the user wants to facet the boxplot else False",type:"bool"},facet_col:{name:"facet_col",default:null,description:"column name to use for faceting or None",type:"DBColumn"},color:{name:"color",description:"color to use for the boxplot",default:["#000000","#009D94","#0057CF","#FFBD00","#FF5C1C","#691A6B"],type:"DropdownSingleSelect"},opacity:{name:"opacity",default:[.1,.2,.3,.4,.5],description:"numerical value between 0 and 1",type:"DropdownSingleSelect"}},toolbox:"plots",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]},heatmap:{name:"heatmap",function_name:"Heatmap",description:"Generates a heatmap using python's seaborn library. This accepts the full dataset as the first parameter, and not summary statistics or aggregates.",input_metadata:{full_data:{name:"full_data",default:null,description:"input_df_name",type:"pandas.core.frame.DataFrame"},x_position_column:{name:"x_position_column",default:null,description:"heatmap_x_column",type:"DBColumn"},y_position_column:{name:"y_position_column",default:null,description:"heatmap_y_column",type:"DBColumn"},color_column:{name:"color_column",default:null,description:"heatmap_value_column",type:"DBColumn"},aggregation_type:{name:"aggregation_type",default:["mean","median","max","min","sum"],description:"a string (can be mean, median, max, min or sum)",type:"DropdownSingleSelect"},color_scale:{name:"color_scale",description:"color_scale (only if specified by the user. defaults to YlGnBu)",default:["magma","inferno","plasma","viridis","cividis","twilight","twilight_shifted","turbo","Blues","BrBG","BuGn","BuPu","CMRmap","GnBu","Greens","Greys","OrRd","Oranges","PRGn","PiYG","PuBu","PuBuGn","PuOr","PuRd","Purples","RdBu","RdGy","RdPu","RdYlBu","RdYlGn","Reds","Spectral","Wistia","YlGn","YlGnBu","YlOrBr","YlOrRd","afmhot","autumn","binary","bone","brg","bwr","cool","coolwarm","copper","cubehelix","flag","gist_earth","gist_gray","gist_heat","gist_ncar","gist_rainbow","gist_stern","gist_yarg","gnuplot","gnuplot2","gray","hot","hsv","jet","nipy_spectral","ocean","pink","prism","rainbow","seismic","spring","summer","terrain","winter","Accent","Dark2","Paired","Pastel1","Pastel2","Set1","Set2","Set3","tab10","tab20","tab20b","tab20c","grey","gist_grey","gist_yerg","Grays","magma_r","inferno_r","plasma_r","viridis_r","cividis_r","twilight_r","twilight_shifted_r","turbo_r","Blues_r","BrBG_r","BuGn_r","BuPu_r","CMRmap_r","GnBu_r","Greens_r","Greys_r","OrRd_r","Oranges_r","PRGn_r","PiYG_r","PuBu_r","PuBuGn_r","PuOr_r","PuRd_r","Purples_r","RdBu_r","RdGy_r","RdPu_r","RdYlBu_r","RdYlGn_r","Reds_r","Spectral_r","Wistia_r","YlGn_r","YlGnBu_r","YlOrBr_r","YlOrRd_r","afmhot_r","autumn_r","binary_r","bone_r","brg_r","bwr_r","cool_r","coolwarm_r","copper_r","cubehelix_r","flag_r","gist_earth_r","gist_gray_r","gist_heat_r","gist_ncar_r","gist_rainbow_r","gist_stern_r","gist_yarg_r","gnuplot_r","gnuplot2_r","gray_r","hot_r","hsv_r","jet_r","nipy_spectral_r","ocean_r","pink_r","prism_r","rainbow_r","seismic_r","spring_r","summer_r","terrain_r","winter_r","Accent_r","Dark2_r","Paired_r","Pastel1_r","Pastel2_r","Set1_r","Set2_r","Set3_r","tab10_r","tab20_r","tab20b_r","tab20c_r","rocket","rocket_r","mako","mako_r","icefire","icefire_r","vlag","vlag_r","flare","flare_r","crest","crest_r"],type:"DropdownSingleSelect"}},toolbox:"plots",output_metadata:[{name:"output_df",description:"pandas dataframe",type:"pandas.core.frame.DataFrame"}]}};var i=a(76174),s=a(86447);let getAnalysis=async e=>{let t;let a=(0,r.Z)("http","get_report");try{t=await fetch(a,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({report_id:e})})}catch(e){return{success:!1,error_message:e}}let n=await t.json();return n},createAnalysis=async function(e){let t,a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},o=(0,r.Z)("http","create_analysis");try{t=await fetch(o,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({custom_id:a,token:e,...n})})}catch(e){return{success:!1,error_message:e}}let l=await t.json();return l},getAllDocs=async e=>{let t=(0,r.Z)("http","get_docs");try{return(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({token:e})})).json()}catch(e){return{success:!1,error_message:e}}},u=getAllDocs,getTableData=async e=>{let t=(0,r.Z)("http","get_table_chart");try{return(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({table_id:e})})).json()}catch(e){return{success:!1,error_message:e}}},getAllAnalyses=async()=>{let e=(0,r.Z)("http","get_analyses");try{return(await fetch(e,{method:"POST",headers:{"Content-Type":"application/json"}})).json()}catch(e){return{success:!1,error_message:e}}},getToolboxes=async e=>{let t=(0,r.Z)("http","get_toolboxes");try{return(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({token:e})})).json()}catch(e){return{success:!1,error_message:e}}},getCursorColor=function(){let e="#000",t=(0,n.random)().hex(),a=(0,n.contrast)(t,e);for(;a<9;)t=(0,n.random)().hex(),a=(0,n.contrast)(t,e);return t},c=["analysis","table-chart"],roundNumber=function(e){return null==e?null:e<1&&e>-1||e>1e5||e<-1e5?e.toExponential(2):Math.round(100*e)/100},getToolRunData=async e=>{let t=(0,r.Z)("http","get_tool_run");try{return(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({tool_run_id:e})})).json()}catch(e){return{success:!1,error_message:e}}},isNullOrUndefined=function(e){return null==e},deleteDoc=async e=>{let t=(0,r.Z)("http","delete_doc");try{return(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({doc_id:e})})).json()}catch(e){return{success:!1,error_message:e}}},d={data_fetcher_and_aggregator:"Fetch data from db",global_dict_data_fetcher_and_aggregator:"Query data",line_plot:"Line Plot",kaplan_meier_curve:"Kaplan Meier Curve",hazard_ratio:"Hazard Ratio",t_test:"T Test",anova_test:"ANOVA Test",wilcoxon_test:"Wilcoxon Test",boxplot:"Boxplot",heatmap:"Heatmap",fold_change:"Fold Change"},m={data_fetcher_and_aggregator:"Fetch ",global_dict_data_fetcher_and_aggregator:"Query ",line_plot:"Line",kaplan_meier_curve:"KM Curve",hazard_ratio:"Hazard Ratio",t_test:"T Test",anova_test:"ANOVA Test",wilcoxon_test:"Wilcoxon Test",boxplot:"Boxplot",heatmap:"Heatmap",fold_change:"Fold Change"},p={DBColumn:"Column name",DBColumnList:"List of column names","pandas.core.frame.DataFrame":"Dataframe",str:"String",int:"Integer",float:"Float",bool:"Boolean","list[str]":"List of strings",list:"List",DropdownSingleSelect:"String"},f={cancer_survival:"Cancer Survival",data_fetching:"Data Fetching",plots:"Plots",stats:"Stats"};function createInitialToolInputs(e,t){let a={};return Object.values(l[e].input_metadata).forEach(e=>{if("pandas.core.frame.DataFrame"===e.type)try{a[e.name]="global_dict."+(null==t?void 0:t[0])}catch(e){console.log(e)}else a[e.name]=Array.isArray(e.default)?e.default[0]:e.default}),a}function arrayOfObjectsToObject(e,t){let a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null;return e.reduce((e,n)=>(e[n[t]]=Object.keys(n).reduce((e,t)=>(Array.isArray(a)&&!a.includes(t)||(e[t]=n[t]),e),{}),e),{})}function parseData(e){let t=(0,i.ueB)(e),a=t.columns,n=t.map(e=>Object.values(e)),r=(0,s.LS)(n,a);return r.newCols.forEach((e,t)=>{e.numeric&&r.newRows.forEach(t=>{t[e.title]=Number(null==t?void 0:t[e.title])})}),{columns:r.newCols,data:r.newRows}}o.q6.define();let g=(0,r.Z)("http","add_tool"),addTool=async e=>{let{tool_name:t,function_name:a,description:n,code:r,input_metadata:o,output_metadata:l,toolbox:i,no_code:s=!1}=e;try{let e=await fetch(g,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({tool_name:t,function_name:a,description:n,code:r,input_metadata:o,output_metadata:l,toolbox:i,no_code:s})}),u=await e.json();return u}catch(e){return console.error(e),{success:!1,error_message:e}}},deleteToolRunIds=async(e,t)=>{let a=(0,r.Z)("http","delete_steps");try{let n=await fetch(a,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({analysis_id:e,tool_run_ids:t})}).then(e=>e.json());return n}catch(e){return console.error(e),{success:!1,error_message:e}}}}}]);