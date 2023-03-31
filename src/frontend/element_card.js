function search_nonworld_element_cards(world_id) {
    return (
            <div className="card-grid">
            <a className="card" href="#">
                <div className="card__background"
    style="background-image: url(https://images.unsplash.com/photo-1557177324-56c542165309?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80)"/>
                <div className="card__content">
                    <p className="card__category">Category</p>
                    <h3 className="card__heading">Example Card Heading</h3>
                </div>
            </a>
            <a className="card" href="#">
                <div className="card__background"
    style="background-image: url(https://images.unsplash.com/photo-1557187666-4fd70cf76254?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60)"/>
                <div className="card__content">
                    <p className="card__category">Category</p>
                    <h3 className="card__heading">Example Card Heading</h3>
                </div>
            </a>
        </div>
    )
}