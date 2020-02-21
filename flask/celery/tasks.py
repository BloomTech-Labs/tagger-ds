@app.task(bind=True, name='refresh')
def train_model(self):
        # Get JSON and convert to DataFrame
        j = json.loads(request.data)
        df = pd.DataFrame(data=j["emails"])

        # Embed emails
        basilica_client.df = df
        df = basilica_client.embed_basilica_to_df()

        # Train model
        X = np.vstack(np.array(df['embedded']))
        y = df["id_email"].values
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X, y)

        # Save/compress model's pickle into the database
        file_obj = BytesIO() 
        joblib.dump(knn, file_obj, compress=3)
        file_obj.seek(0)
        pkl = file_obj.getvalue()

        # Check if user already exists
        db_user = User.query.filter(User.email_address == j["address"]).scalar()
        if db_user: 
            # Update pickle if user exists
            db_user.pickle_file = pkl
        else:
            # Make new user if one doesn't exist
            db_user = User(email_address=j["address"], pickle_file=pkl)
            DB.session.add(db_user)
        DB.session.commit()
        file_obj.close()
        return "Trained a model!"