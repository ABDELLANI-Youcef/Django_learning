import React from 'react';
import Header from '../partials/Header';
import Footer from '../partials/Footer';
import { Await, Link, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import apiInstance from '../../utils/axios';
import Moment from '../../plugin/Moment';
import Toast from "../../plugin/Toast";

function Detail() {
  const [post, setPost] = useState([]);
  const [tags, setTags] = useState([]);
  const [createComment, setCreateComment] = useState({full_name: "", email: "", comment: ""})

  const param = useParams();

  const fetchPost = async () => {
    const response = await apiInstance.get(`post/detail/${param.slug}/`);
    setPost(response.data);

    const tagArray = response.data?.tags?.split(',');
    setTags(tagArray);
  };

  useEffect(() => {
    fetchPost();
  }, []);

  const handleCreateCommentChange = (event) =>{
    setCreateComment(
      {...createComment,
      [event.target.name]: event.target.value}
    )
  }

  const handleCreateCommentSubmit = async (event) => {
    event.preventDefault()

    const json = {
      post_id: post?.id,
      name: createComment.full_name,
      email: createComment.email,
      comment: createComment.comment
    }
    const response = await apiInstance.post('post/comment-post/', json)
    console.log(response);
    Toast("success", "Comment Posted")

    setCreateComment(
      {
        full_name: "",
        email: "",
        comment: ""
      }
    )
  }

  return (
    <>
      <Header />
      <section className=" mt-5">
        <div className="container">
          <div className="row">
            <div className="col-12">
              <a href="#" className="badge bg-danger mb-2 text-decoration-none">
                <i className="small fw-bold " />
                Lifestyle
              </a>
              <h1 className="text-center">
                {post?.title}
              </h1>
            </div>
          </div>
        </div>
      </section>

      <section className="pt-0">
        <div className="container position-relative" data-sticky-container="">
          <div className="row">
            <div className="col-lg-2">
              <div
                className="text-start text-lg-center mb-5"
                data-sticky=""
                data-margin-top={80}
                data-sticky-for={991}
              >
                <div className="position-relative">
                  <div className="avatar avatar-xl">
                    <img
                      className="avatar-img"
                      style={{
                        width: '100px',
                        height: '100px',
                        objectFit: 'cover',
                        borderRadius: '50%',
                      }}
                      src={post?.profile?.image}
                      alt="avatar"
                    />
                  </div>
                  <a
                    href="#"
                    className="h5 fw-bold text-dark text-decoration-none mt-2 mb-0 d-block"
                  >
                    {post?.profile?.full_name}
                  </a>
                  <p>{post?.profile?.bio || ""}</p>
                </div>

                <hr className="d-none d-lg-block " />

                <ul className="list-inline list-unstyled">
                  <li className="list-inline-item d-lg-block my-lg-2 text-start">
                    <i className="fas fa-calendar"></i> {Moment(post?.date)}
                  </li>
                  {/* <li className="list-inline-item d-lg-block my-lg-2 text-start">
                    <i className="fas fa-clock"></i> 5 min read
                  </li> */}
                  <li className="list-inline-item d-lg-block my-lg-2 text-start">
                    <a href="#" className="text-body">
                      <i className="fas fa-heart me-1" />
                    </a>
                    {post?.likes?.length} Likes
                  </li>
                  <li className="list-inline-item d-lg-block my-lg-2 text-start">
                    <i className="fas fa-eye" />
                    {post?.view}
                  </li>
                </ul>
                {/* Tags */}
                <ul className="list-inline text-primary-hover mt-0 mt-lg-3 text-start">
                  {tags?.map((tag, index)=>(
                    <li className="list-inline-item" key={index}>
                      <a
                        className="text-body text-decoration-none fw-bold"
                        href="#"
                      >
                        #{tag}
                      </a>
                    </li>))
                  }
                </ul>
              </div>
            </div>
            {/* Left sidebar END */}
            {/* Main Content START */}
            <div className="col-lg-10 mb-5">
              <p>
               {post?.description}
              </p>
              {/* <div className="mt-5">
                <h2 className="my-3">
                  <i className="bi bi-symmetry-vertical me-2" />
                  Related post
                </h2>
                <section className="pt-4 pb-0">
                  <div className="container">
                    <div className="row">
                      <div className="col-sm-6 col-lg-3">
                        <div className="card mb-4">
                          <div className="card-fold position-relative">
                            <img
                              className="card-img"
                              style={{
                                width: '100%',
                                height: '160px',
                                objectFit: 'cover',
                              }}
                              src="https://awcdn1.ahmad.works/writing/wp-content/uploads/2015/05/kitchen-and-dining-room-P5JHHM6.jpg"
                              alt="Card image"
                            />
                          </div>
                          <div className="card-body px-3 pt-3">
                            <h4 className="card-title">
                              <Link
                                to={`/7-common-mistakes-everyone-makes-while-travelling/`}
                                className="btn-link text-reset stretched-link fw-bold text-decoration-none"
                              >
                                7 common mistakes everyone makes while traveling
                              </Link>
                            </h4>
                          </div>
                        </div>
                      </div>

                      <div className="col-sm-6 col-lg-3">
                        <div className="card mb-4">
                          <div className="card-fold position-relative">
                            <img
                              className="card-img"
                              style={{
                                width: '100%',
                                height: '160px',
                                objectFit: 'cover',
                              }}
                              src="https://awcdn1.ahmad.works/writing/wp-content/uploads/2015/05/black-woman-smiling-with-hands-in-hair-PMCFL93-1.jpg"
                              alt="Card image"
                            />
                          </div>
                          <div className="card-body px-3 pt-3">
                            <h4 className="card-title">
                              <a
                                href="post-single.html"
                                className="btn-link text-reset stretched-link fw-bold text-decoration-none"
                              >
                                7 common mistakes everyone makes while traveling
                              </a>
                            </h4>
                          </div>
                        </div>
                      </div>

                      <div className="col-sm-6 col-lg-3">
                        <div className="card mb-4">
                          <div className="card-fold position-relative">
                            <img
                              className="card-img"
                              style={{
                                width: '100%',
                                height: '160px',
                                objectFit: 'cover',
                              }}
                              src="https://awcdn1.ahmad.works/writing/wp-content/uploads/2015/05/flat-with-touch-of-creativity-PX387LV-2.jpg"
                              alt="Card image"
                            />
                          </div>
                          <div className="card-body px-3 pt-3">
                            <h4 className="card-title">
                              <a
                                href="post-single.html"
                                className="btn-link text-reset stretched-link fw-bold text-decoration-none"
                              >
                                7 common mistakes everyone makes while traveling
                              </a>
                            </h4>
                          </div>
                        </div>
                      </div>

                      <div className="col-sm-6 col-lg-3">
                        <div className="card mb-4">
                          <div className="card-fold position-relative">
                            <img
                              className="card-img"
                              style={{
                                width: '100%',
                                height: '160px',
                                objectFit: 'cover',
                              }}
                              src="https://awcdn1.ahmad.works/writing/wp-content/uploads/2015/05/young-handsome-afro-black-man-going-upstairs-from-PJWPWPR-2.jpg"
                              alt="Card image"
                            />
                          </div>
                          <div className="card-body px-3 pt-3">
                            <h4 className="card-title">
                              <a
                                href="post-single.html"
                                className="btn-link text-reset stretched-link fw-bold text-decoration-none"
                              >
                                7 common mistakes everyone makes while traveling
                              </a>
                            </h4>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>
              </div> */}

              <hr />
              <div className="d-flex py-4">
                <a href="#">
                  <div className="avatar avatar-xxl me-4">
                    <img
                      className="avatar-img rounded-circle"
                      src={post?.profile?.image}
                      style={{
                        width: '100px',
                        height: '100px',
                        objectFit: 'cover',
                        borderRadius: '50%',
                      }}
                      alt="avatar"
                    />
                  </div>
                </a>
                <div>
                  <div className="d-sm-flex align-items-center justify-content-between">
                    <div>
                      <h4 className="m-0">
                        <a href="#" className="text-dark text-decoration-none">
                          {post?.user?.username}
                        </a>
                      </h4>
                      <small>{post?.profile?.about}</small>
                    </div>
                  </div>
                  <p className="my-2">
                    {post?.profile?.bio}
                  </p>
                  {/* Social icons */}
                  <ul className="nav">
                    <li className="nav-item">
                      <a className="nav-link ps-0 pe-2 fs-5" href="#">
                        <i className="fab fa-facebook-square" />
                      </a>
                    </li>
                    <li className="nav-item">
                      <a className="nav-link px-2 fs-5" href="#">
                        <i className="fab fa-twitter-square" />
                      </a>
                    </li>
                    <li className="nav-item">
                      <a className="nav-link px-2 fs-5" href="#">
                        <i className="fab fa-linkedin" />
                      </a>
                    </li>
                  </ul>
                </div>
              </div>

              <div>
                <h3>{post?.comments?.length} comments</h3>
                {post?.comments?.map((comment, index)=> (
                  <div className="my-4 d-flex bg-light p-3 mb-3 rounded" key={index}>
                    {/* <img
                      className="avatar avatar-md rounded-circle float-start me-3"
                      src="https://img.freepik.com/free-photo/front-portrait-woman-with-beauty-face_186202-6146.jpg?size=626&ext=jpg&ga=GA1.1.735520172.1710979200&semt=ais"
                      style={{
                        width: '70px',
                        height: '70px',
                        objectFit: 'cover',
                        borderRadius: '50%',
                      }}
                      alt="avatar"
                    /> */}
                    <div>
                      <div className="mb-2">
                        <h5 className="m-0">{comment?.name}</h5>
                        <span className="me-3 small">{Moment(comment.date)}</span>
                      </div>
                      <p className="fw-bold">
                        {comment?.comment}
                      </p>
                    </div>
                  </div>))
                  }

              </div>
              {/* Comments END */}
              {/* Reply START */}
              <div className="bg-light p-3 rounded">
                <h3 className="fw-bold">Leave a reply</h3>
                <small>
                  Your email address will not be published. Required fields are
                  marked *
                </small>
                <form className="row g-3 mt-2" onSubmit={handleCreateCommentSubmit}>
                  <div className="col-md-6">
                    <label className="form-label">Name *</label>
                    <input
                      type="text"
                      className="form-control"
                      aria-label="First name"
                      onChange={handleCreateCommentChange}
                      name='full_name'
                      value={createComment.full_name}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label" >Email *</label>
                    <input
                      type="email"
                      className="form-control"
                      onChange={handleCreateCommentChange}
                      name='email'
                      value={createComment.email}
                    />
                  </div>
                  <div className="col-12">
                    <label className="form-label" >Write Comment *</label>
                    <textarea
                      className="form-control"
                      rows={4}
                      onChange={handleCreateCommentChange}
                      name="comment"
                      value={createComment.comment}
                    />
                  </div>
                  <div className="col-12">
                    <button type="submit" className="btn btn-primary">
                      Post comment <i className="fas fa-paper-plane"></i>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </>
  );
}

export default Detail;
