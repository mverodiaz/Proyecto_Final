const { createApp } = Vue
  createApp({
    data() {
      return {
        PickUps:[],
        url:'http://localhost:5000/pickups', 
        error:false,
        cargando:true,
        /*atributos para el guardar los valores del formulario */
        id:0,
        nombre:"", 
        imagen:"",
        stock:"",
        precio:"",
    }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.PickUps = data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        eliminar(PickUp) {
            if (!confirm("¿Confirma que desea eliminar este registro?")){
                return;
            }
            const url = this.url+'/' + PickUp;
            var options = {
                method: 'DELETE',
            }
            fetch(url, options)
                .then(res => res.text()) // or res.json()
                .then(res => {
                    location.reload();
                })
        },
        grabar(){
            let PickUp = {
                nombre:this.nombre,
                precio: this.precio,
                stock: this.stock,
                imagen:this.imagen
            }
            var options = {
                body:JSON.stringify(PickUp),
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro grabado")
                    window.location.href = "./pickups.html";  
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Grabar")
                })      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')