var tableTemplate = `
<table>
    <thead>
        {{#headers}}
             {{#.}}
            <th>{{.}}</th>
             {{/.}}
        {{/headers}}
     </thead>
     <tbody>
         {{#items}}
             <tr>
                 {{#.}}
                     <td>{{.}}</td>
                 {{/.}}
           </tr>
         {{/items}}
     </tbody>
</table>
`;
var errorTemplate = `
错误<br>
<div>{{error}}<div>
`;
var statusTemplate = `
<br>
<div>{{status}}<div>
`;
