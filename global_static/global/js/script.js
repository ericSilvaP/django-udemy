function my_scope() {
    const forms = document.querySelectorAll('.delete-recipe-form')
    for (const form of forms) {
        form.addEventListener('submit', (e) => {
            e.preventDefault()

            const confirmed = confirm('Deletar receita?')

            if (confirmed) {
                form.submit()
            }
        })
    }
}

my_scope()
