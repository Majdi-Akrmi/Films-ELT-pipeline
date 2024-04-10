{% set film_title = 'Avatar' %}

SELECT * 
FROM {{ ref('films') }}
WHERE title = '{{ film_title }}'