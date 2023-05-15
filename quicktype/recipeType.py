from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class AggregateRating:
    rating_value: Optional[str] = None
    rating_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AggregateRating':
        assert isinstance(obj, dict)
        rating_value = from_union([from_str, from_none], obj.get("ratingValue"))
        rating_count = from_union([from_int, from_none], obj.get("ratingCount"))
        return AggregateRating(rating_value, rating_count)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.rating_value is not None:
            result["ratingValue"] = from_union([from_str, from_none], self.rating_value)
        if self.rating_count is not None:
            result["ratingCount"] = from_union([from_int, from_none], self.rating_count)
        return result


@dataclass
class RecipeImage:
    type: Optional[str] = None
    url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'RecipeImage':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        height = from_union([from_int, from_none], obj.get("height"))
        width = from_union([from_int, from_none], obj.get("width"))
        return RecipeImage(type, url, height, width)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        return result


@dataclass
class ImageElement:
    type: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ImageElement':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        return ImageElement(type, url)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class Instruction:
    type: Optional[str] = None
    text: Optional[str] = None
    image: Optional[List[ImageElement]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Instruction':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        text = from_union([from_str, from_none], obj.get("text"))
        image = from_union([from_none, lambda x: from_list(ImageElement.from_dict, x)], obj.get("image"))
        return Instruction(type, text, image)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.text is not None:
            result["text"] = from_union([from_str, from_none], self.text)
        if self.image is not None:
            result["image"] = from_union([from_none, lambda x: from_list(lambda x: to_class(ImageElement, x), x)], self.image)
        return result


@dataclass
class Nutrition:
    calories: Optional[int] = None
    carbohydrate: Optional[int] = None
    cholesterol: Optional[int] = None
    fiber: Optional[int] = None
    protein: Optional[int] = None
    saturated_fat: Optional[int] = None
    sodium: Optional[int] = None
    sugar: Optional[int] = None
    fat: Optional[int] = None
    unsaturated_fat: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Nutrition':
        assert isinstance(obj, dict)
        calories = from_union([from_int, from_none], obj.get("calories"))
        carbohydrate = from_union([from_int, from_none], obj.get("carbohydrate"))
        cholesterol = from_union([from_int, from_none], obj.get("cholesterol"))
        fiber = from_union([from_int, from_none], obj.get("fiber"))
        protein = from_union([from_int, from_none], obj.get("protein"))
        saturated_fat = from_union([from_int, from_none], obj.get("saturatedFat"))
        sodium = from_union([from_int, from_none], obj.get("sodium"))
        sugar = from_union([from_int, from_none], obj.get("sugar"))
        fat = from_union([from_int, from_none], obj.get("fat"))
        unsaturated_fat = from_union([from_int, from_none], obj.get("unsaturatedFat"))
        return Nutrition(calories, carbohydrate, cholesterol, fiber, protein, saturated_fat, sodium, sugar, fat, unsaturated_fat)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.calories is not None:
            result["calories"] = from_union([from_int, from_none], self.calories)
        if self.carbohydrate is not None:
            result["carbohydrate"] = from_union([from_int, from_none], self.carbohydrate)
        if self.cholesterol is not None:
            result["cholesterol"] = from_union([from_int, from_none], self.cholesterol)
        if self.fiber is not None:
            result["fiber"] = from_union([from_int, from_none], self.fiber)
        if self.protein is not None:
            result["protein"] = from_union([from_int, from_none], self.protein)
        if self.saturated_fat is not None:
            result["saturatedFat"] = from_union([from_int, from_none], self.saturated_fat)
        if self.sodium is not None:
            result["sodium"] = from_union([from_int, from_none], self.sodium)
        if self.sugar is not None:
            result["sugar"] = from_union([from_int, from_none], self.sugar)
        if self.fat is not None:
            result["fat"] = from_union([from_int, from_none], self.fat)
        if self.unsaturated_fat is not None:
            result["unsaturatedFat"] = from_union([from_int, from_none], self.unsaturated_fat)
        return result


@dataclass
class Review:
    name: Optional[str] = None
    rating: Optional[int] = None
    body: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Review':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        rating = from_union([from_int, from_none], obj.get("rating"))
        body = from_union([from_str, from_none], obj.get("body"))
        return Review(name, rating, body)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.rating is not None:
            result["rating"] = from_union([from_int, from_none], self.rating)
        if self.body is not None:
            result["body"] = from_union([from_str, from_none], self.body)
        return result


@dataclass
class Video:
    type: Optional[str] = None
    embed_url: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    name: Optional[str] = None
    thumbnail_url: Optional[str] = None
    upload_date: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Video':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        embed_url = from_union([from_str, from_none], obj.get("embed_url"))
        description = from_union([from_str, from_none], obj.get("description"))
        duration = from_union([from_str, from_none], obj.get("duration"))
        name = from_union([from_str, from_none], obj.get("name"))
        thumbnail_url = from_union([from_str, from_none], obj.get("thumbnail_url"))
        upload_date = from_union([from_datetime, from_none], obj.get("upload_date"))
        return Video(type, embed_url, description, duration, name, thumbnail_url, upload_date)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.embed_url is not None:
            result["embed_url"] = from_union([from_str, from_none], self.embed_url)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.duration is not None:
            result["duration"] = from_union([from_str, from_none], self.duration)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.thumbnail_url is not None:
            result["thumbnail_url"] = from_union([from_str, from_none], self.thumbnail_url)
        if self.upload_date is not None:
            result["upload_date"] = from_union([lambda x: x.isoformat(), from_none], self.upload_date)
        return result


@dataclass
class Recipe:
    url: Optional[str] = None
    category: Optional[List[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[List[Instruction]] = None
    image: Optional[RecipeImage] = None
    video: Optional[Video] = None
    date_published: Optional[datetime] = None
    servings: Optional[int] = None
    cook_time: Optional[str] = None
    prep_time: Optional[str] = None
    reviews: Optional[List[Review]] = None
    aggregate_rating: Optional[AggregateRating] = None
    nutrition: Optional[Nutrition] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Recipe':
        assert isinstance(obj, dict)
        url = from_union([from_str, from_none], obj.get("url"))
        category = from_union([lambda x: from_list(from_str, x), from_none], obj.get("category"))
        title = from_union([from_str, from_none], obj.get("title"))
        description = from_union([from_str, from_none], obj.get("description"))
        ingredients = from_union([lambda x: from_list(from_str, x), from_none], obj.get("ingredients"))
        instructions = from_union([lambda x: from_list(Instruction.from_dict, x), from_none], obj.get("instructions"))
        image = from_union([RecipeImage.from_dict, from_none], obj.get("image"))
        if obj.get("video") != 'No Video':
            video = from_union([Video.from_dict, from_none], obj.get("video"))
        else:
            video = 'No Video'
        date_published = from_union([from_datetime, from_none], obj.get("datePublished"))
        servings = from_union([from_int, from_none], obj.get("servings"))
        cook_time = from_union([from_str, from_none], obj.get("cookTime"))
        prep_time = from_union([from_str, from_none], obj.get("prepTime"))
        reviews = from_union([lambda x: from_list(Review.from_dict, x), from_none], obj.get("reviews"))
        aggregate_rating = from_union([AggregateRating.from_dict, from_none], obj.get("aggregateRating"))
        nutrition = from_union([Nutrition.from_dict, from_none], obj.get("nutrition"))
        return Recipe(url, category, title, description, ingredients, instructions, image, video, date_published, servings, cook_time, prep_time, reviews, aggregate_rating, nutrition)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.url is not None:
            result["url"] = from_union([from_str, from_none], self.url)
        if self.category is not None:
            result["category"] = from_union([lambda x: from_list(from_str, x), from_none], self.category)
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.ingredients is not None:
            result["ingredients"] = from_union([lambda x: from_list(from_str, x), from_none], self.ingredients)
        if self.instructions is not None:
            result["instructions"] = from_union([lambda x: from_list(lambda x: to_class(Instruction, x), x), from_none], self.instructions)
        if self.image is not None:
            result["image"] = from_union([lambda x: to_class(RecipeImage, x), from_none], self.image)
        if self.video is not None:
            result["video"] = from_union([lambda x: to_class(Video, x), from_none], self.video)
        if self.date_published is not None:
            result["datePublished"] = from_union([lambda x: x.isoformat(), from_none], self.date_published)
        if self.servings is not None:
            result["servings"] = from_union([from_int, from_none], self.servings)
        if self.cook_time is not None:
            result["cookTime"] = from_union([from_str, from_none], self.cook_time)
        if self.prep_time is not None:
            result["prepTime"] = from_union([from_str, from_none], self.prep_time)
        if self.reviews is not None:
            result["reviews"] = from_union([lambda x: from_list(lambda x: to_class(Review, x), x), from_none], self.reviews)
        if self.aggregate_rating is not None:
            result["aggregateRating"] = from_union([lambda x: to_class(AggregateRating, x), from_none], self.aggregate_rating)
        if self.nutrition is not None:
            result["nutrition"] = from_union([lambda x: to_class(Nutrition, x), from_none], self.nutrition)
        return result


def recipe_from_dict(s: Any) -> Recipe:
    return Recipe.from_dict(s)


def recipe_to_dict(x: Recipe) -> Any:
    return to_class(Recipe, x)



