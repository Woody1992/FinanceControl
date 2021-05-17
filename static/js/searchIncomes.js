const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const noResult = document.querySelector('.no-results');
const paginationContainer = document.querySelector('.pagination-container')
const tableBody = document.querySelector('.table-body')
const url = 'http://127.0.0.1:8000/'
tableOutput.style.display= 'none';
searchField.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value;
    console.log(searchValue)

    if(searchValue.trim().length > 0){
        paginationContainer.style.display= 'none';
        fetch("search-income/", { // where we send api call
            body: JSON.stringify({searchText: searchValue}), // searchText in view.py
            method:'POST',
        })
            .then((res)=>res.json())
            .then((data) =>{
                console.log('data', data);
                appTable.style.display= 'none';
                tableOutput.style.display= 'block';

                if (data.length ===0){
                    tableOutput.style.display= 'none';
                    noResult.style.display= 'block';
                }else {
                    tableBody.innerHTML=''
                    noResult.style.display= 'none';
                    data.forEach(item=>{
                        tableBody.innerHTML+= `
                        <tr>
                            <td>${item.date}</td>
                            <td>${item.amount}</td>
                            <td>${item.source}</td>
                            <td>${item.description}</td>
                            <td>
                            <a href="edit-income/${item.id}"><button type="button" class="btn btn-primary btn-sm btn-outline-primary" style="width: 45%">
                                <i class="far fa-edit"></i>
                            </button></a>
                            <a href="delete-income/${item.id}"><button type="button" data-toggle="modal" data-target="#deleteModal" class="btn btn-secondary btn-sm btn-outline-danger" style="width: 45%; margin-left: 6%;">
                                <i class="fas fa-trash"></i>
                            </button></a>
                            </td>
                        </tr>
                    `
                    })
                }
        })
    }else{
        tableOutput.style.display= 'none'
        noResult.style.display= 'none';
        appTable.style.display= 'block';
        paginationContainer.style.display= 'block';
    }
})