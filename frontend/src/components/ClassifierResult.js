import React, { useState, useEffect } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useTheme } from '@mui/material';

const ClassifierResult = ({ selectedImage, classificationResult }) => {
  const theme = useTheme();
  const [searchValue, setSearchValue] = useState('');
  const [recipes, setRecipes] = useState([]);

  // Automatically set the classification result as the initial search term
  useEffect(() => {
    setSearchValue(classificationResult);
  }, [classificationResult]);

  const searchRecipes = async () => {
    try {
      const response = await fetch(
        `https://api.edamam.com/search?q=${searchValue}&app_id=7aa516a5&app_key=dc836a223fb788b11ae390504d9e97ce&from=0&to=10`
      );
      const data = await response.json();
      setRecipes(data.hits);
    } catch (error) {
      console.error('Error fetching recipes:', error);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    searchRecipes();
  };

  const displayRecipes = (recipes) => {
    return recipes.map((recipe) => (
      <div key={recipe.recipe.uri}>
        <img src={recipe.recipe.image} alt={recipe.recipe.label} />
        <h3>{recipe.recipe.label}</h3>
        <ul>
          {recipe.recipe.ingredientLines.map((ingredient, index) => (
            <li key={index}>{ingredient}</li>
          ))}
        </ul>
        <a href={recipe.recipe.url} target="_blank" rel="noopener noreferrer">
          View Recipe
        </a>
      </div>
    ));
  };

  return (
    <Grid item xs={12}>
      <Card>
        <CardContent>
          <div>
            <div
              style={{
                display: 'flex',
                justifyContent: 'center',
                marginBottom: theme.spacing(2),
                marginTop: theme.spacing(1),
              }}
            >
              <Typography variant='h2' align='center' gutterBottom>
                Result
              </Typography>
            </div>
            <div
              style={{
                flexDirection: 'flex',
                justifyContent: 'center',
              }}
            >
              <Typography variant='subtitle1' align='center' gutterBottom>
                The image you have selected:
              </Typography>
              <div
                style={{
                  transition: 'all .2s ease-in-out',
                  '&:hover': {
                    transform: `translateY(-${theme.spacing(1 / 2)})`,
                  },
                }}
              >
                <img
                  src={selectedImage}
                  height='250'
                  style={{
                    display: 'block',
                    margin: '0 auto',
                    boxShadow: '6px 6px 3px #c5c5c5',
                    borderRadius: '25px',
                  }}
                  alt='Selected'
                />
              </div>
              <br />
              <Typography variant='subtitle1' align='center' gutterBottom>
                The machine learning model has classified this image as:
              </Typography>
              <Typography
                variant='h3'
                color='primary'
                align='center'
                gutterBottom
              >
                {classificationResult}
              </Typography>
            </div>
          </div>
        </CardContent>
      </Card>
      <br />
      <Card>
        <CardContent>
          <form onSubmit={handleSearchSubmit}>
            <TextField
              id='search'
              label='Search for Recipes'
              variant='outlined'
              fullWidth
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
            />
            <br />
            <br />
            <Button
              variant='contained'
              color='primary'
              type='submit'
              disabled={!searchValue.trim()}
            >
              Search
            </Button>
          </form>
          <br />
          {recipes.length > 0 && (
            <div>
              <Typography variant='h4' align='center' gutterBottom>
                Recipes
              </Typography>
              {displayRecipes(recipes)}
            </div>
          )}
        </CardContent>
      </Card>
    </Grid>
  );
};

export default ClassifierResult;